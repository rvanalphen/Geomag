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