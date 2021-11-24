from pandas.core.frame import DataFrame
from pydantic import BaseModel, validator
from pathlib import Path, Path
from typing import Dict, List, Union
from pydantic.main import UNTOUCHED_TYPES
from pyproj import CRS
from pprint import pprint

from source.load_data import path_to_df

class Models(BaseModel):
    line: DataFrame
    shapes: List[Union[Path,str]]
    top_bound: List[Union[float,int]]
    bottom_bound: int
    inclination: int
    declination: int
    intensity: Union[float,int]
    shape_dict: Dict = None

    # no current pydantic way to validate dataframe
    class Config:
        arbitrary_types_allowed = True

    @validator('shapes',each_item=True)
    def path_validator(cls, f) -> Path:
        if not f.is_file():
            raise AttributeError(
                'The file specified does not exist; check filepath')
        return f

    @validator('top_bound',each_item=True)
    def top_validator(cls,bnd):
        if type(bnd) != float and type(bnd) != int:
            raise TypeError("Top bounds %i must be an int" % bnd)
        return bnd

    @validator('bottom_bound','inclination','declination',allow_reuse=True)
    def other_validator(cls, num) -> int:
        if type(num) != int:
            raise TypeError("Value %i must be an int" % num)
        return num

    @validator('intensity')
    def other_validator(cls, mi) -> Union[float,int]:
        print(mi)
        if type(mi) != float and type(mi) != int:
            raise TypeError("intensity must be an int or float")
        return mi


class PloufModel(Models):

    @property
    def Parameters(self):
        pprint(self.dict(exclude={'line'},exclude_unset=True))
    
    def _shapes_path_to_list(self):
        shape_d = {}
        for i,shape in enumerate(self.shapes):
            name = 'shape %i' % (i+1)
            shape_d[name] = path_to_df(shape)

        self.shape_dict = shape_d

    def _center_line(self,x0: int, y0: int):

        #Centering data around the middle of Survey Line  
        self.line['Northing'] -= x0
        self.line['Easting'] -= y0
        #Centering anomaly around zero
        mag0 =  self.line.Mag_nT.mean()
        self.line['Mag_nT'] -= mag0

        return self.line

    def _center_shapes(self,x0: int, y0: int):

        for key in self.shape_dict.keys():
            self.shape_dict[key]['Northing'] -= x0
            self.shape_dict[key]['Easting'] -= y0

        return self.shape_dict

    def plouf(self,X,Y,z1,z2,inc,dec,mi,UTM_Line):
        
        from math import cos, sin,pi,sqrt,log,atan2
        from numpy import asarray
        from pandas import DataFrame
        #Setting Parameters
        print('Running Plouf...')
        x = X
        y = Y
        sides=len(X)-1

        #x must be the northing (north coordinate), 
        #y must be the easting (east coordinate),
        #Map coordinates, must be clockwise 

        minc = inc*(pi/180) #down in rad 
        mdec = dec*(pi/180) #east in rad

        #calculate direction cosines of magnetiation
        ml = cos(minc) * cos(mdec)
        mm = cos(minc) * sin(mdec)
        mn = sin(minc)

        #components of magnetization in x,y,z, directions
        mx = mi*ml
        my = mi*mm
        mz = mi*mn

        # set earths field
        einc = 61.6*(pi/180)
        edec = 12*(pi/180)

        el = cos(einc) * cos(edec)
        em = cos(einc) * sin(edec)
        en = sin(einc)

        #proportionality constant 

        prop = 400*pi

        px_list =[]
        b_total_list =[]
    ########################################################
        #insert for J loop
        for j in range(int(UTM_Line.Northing.min()),int(UTM_Line.Northing.max()),1):
        
            #px is the northing of the observation point
            #py is the easting of the observation point
            #northing and easting observation points 
            px = j
            py = 0
        
            #setting volume integral to zero 
            v1 = 0
            v2 = 0
            v3 = 0 
            v4 = 0 
            v5 = 0 
            v6 = 0 
            
            for i in range(sides):
                if i == (sides-1):
                    x1 = x[i]-px
                    y1 = y[i]-py
                    x2 = x[0]-px
                    y2 = y[0]-py
                else:
                    x1 = x[i]-px
                    y1 = y[i]-py
                    x2 = x[i+1]-px
                    y2 = y[i+1]-py
                    
                #calculate geometry 
                delta_x = x2-x1
                delta_y = y2-y1
                delta_s = sqrt(delta_x**2 + delta_y**2)
            
                #avoid division by zero if delta s = 0
                if delta_s == 0:
                    delta_s = 0.1
            
                c = delta_y/delta_s
                s = delta_x/delta_s
                p = ((x1*y2) - (x2*y1))/delta_s
                
                d1 = x1*s + y1*c
                d2 = x2*s + y2*c
                
                r1sq = x1**2 + y1**2
                r2sq = x2**2 + y2**2
                r11 = sqrt(r1sq + z1**2)
                r12 = sqrt(r1sq + z2**2)
                r21 = sqrt(r2sq + z1**2)
                r22 = sqrt(r2sq + z2**2)
                
                f = log((r22+z2)/(r12+z2)*(r11+z1)/(r21+z1))
                q = log((r22+d2)/(r12+d1)*(r11+d1)/(r21+d2))
                w = atan2((z2*d2),(p*r22)) - \
                    atan2((z2*d1),(p*r12)) - \
                    atan2((z1*d2),(p*r21)) + \
                    atan2((z1*d1),(p*r11))
                
                v1 += s*c*f - c*c*w
                v2 += s*c*w + c*c*f
                v3 += c*q
                v4 += -(s*c*f + s*s*w)
                v5 += -(s*q)
                v6 += w
                
            #calculate the components of the magnetic field 
            bx = prop*(mx*v1 + my*v2 + mz* v3);
            by = prop*(mx*v2 + my*v4 + mz* v5);
            bz = prop*(mx*v3 + my*v5 + mz* v6);

            #calculate total anomaly
            #this calculation works for anomaly << total field strength
            b_total = el*bx + em*by + en*bz
        
            px_list.append(px)
            m = asarray(px_list)
                
            b_total_list.append(b_total)
            n = asarray(b_total_list)
            df_dist = DataFrame
            df_dist = df_dist(m,columns=['dist'])
        

            df_mag = DataFrame
            df_mag = df_mag(n,columns=['mag'])
        

            df_model = DataFrame
            df_model = df_dist.join(df_mag)
            #uncomment these lines to check volume integral
            #v4 = -(v1+v6)
            #test = -($v1+$v6)
            #print(v4,test)
        
            #print results 
            # print (px,b_total)

        return df_model
        
    def run_model(self):
        self._shapes_path_to_list()

        x0 = self.line.Northing.mean() 
        y0 = self.line.Easting.mean()

        self.line = self._center_line(x0,y0)
        self.shape_dict = self._center_shapes(x0,y0)

        posX_dict = {}
        posY_dict = {}
        posVx = []
        posVy = []

        ztop_dict ={}
        model_dict = {}
        results = []

        for i, (key,_) in enumerate(self.shape_dict.items()):

            posVx.append(self.shape_dict[key].Northing.tolist())
            x = 'X{}'.format(i+1)
            posX_dict[x] = posVx[i]

            posVy.append(self.shape_dict[key].Easting.tolist())
            y = 'Y{}'.format(i+1)
            posY_dict[y] = posVy[i]

            z = 'Zt{}'.format(i+1)
            ztop_dict[z] = self.top_bound[i]

            print()

            results.append(
                self.plouf(
                    posX_dict[x],posY_dict[y],ztop_dict[z],
                    self.bottom_bound,
                    self.inclination,
                    self.declination,
                    self.intensity,
                    self.line
                    )
                )
            model_num = 'df_model{}'.format(i+1)
            model_dict[model_num] = results[i]

            return model_dict