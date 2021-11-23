    import geopandas as gpd
    import shapely.geometry

    dfp = gpd.GeoDataFrame(
        app.data,
        geometry=app.data.loc[:,["Easting","Northing"]].apply(shapely.geometry.Point, axis=1),
        crs="EPSG:32611",
    )
    
    line = shapely.geometry.LineString(
        [start,end]
    )
    # add a buffer to LineString (hence becomes a polygon)
    DISTANCE = 10 #m
    line = (
        gpd.GeoSeries([line], crs="EPSG:32611").buffer(DISTANCE)
    )
    
    df_near = gpd.GeoDataFrame(geometry=line).sjoin(dfp)
    df = df_near.iloc[:,2:]
    print(df)





    class SingleSeparator(DataSeparator):
    
    def _parameter_calculator(self,line_params: Dict,buffer: int) -> Polygon:
            lines=[]
            for i, (key,value) in enumerate(line_params.items()):
                print(key)
                start = line_params[key][0]
                end = line_params[key][0]
                
                lines.append(
                    LineString([start,end])
                    )

            return lines

    def split(self, data: DataFrame, line_params: Dict, buffer: int) -> DataFrame:
        
        ideal_lines = self._parameter_calculator(line_params,buffer)
        dfp = GeoDataFrame(data,geometry=data.loc[:,["Easting","Northing"]].apply(Point, axis=1))
        
        name='line'
        line_dict = {}
        for i,line in enumerate(ideal_lines):
            print(line)
            print(name+' '+str(i+1))
            
            actual_line = GeoDataFrame(geometry=line).sjoin(dfp)
            
            line_dict[name] =  actual_line.iloc[:,2:]
            
            return line_dict 

