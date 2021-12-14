# mag_class
Python class for processing, visualizing and manipulating geomagnetic survey data

## TODO:

    - DONE: convert data to specified coordinate system
    
    - DONE: detrend global signal from mag
    
    - DONE: plot data points    
    
    - DONE: plot heatmap of data
    
    - DONE (not needed if using pandas, code is one line no need for a function):subsample data
    
    - DONE: seperate data by heading 
    
    - DONE: seperate data into individual lines

    - DONE: grouped lines into single grouped dataframe

    - DONE: outfile for whole file,each line, all in ns,all in ew

    - DONE: remove mean from data

    - DONE: integrate maping with cartopy
    
    - use z of location to only use points within a tolerance of expected flight height 
    
    - integrate wavlet leveling

    - DONE: remove linear trends from line
    
    - possible other ideas: 
    
        - DONE: visualization of individual transects
        - DONE: visualization of sets of transects with an offset,
        - DONE: plouff forward modeling, 
        - running some of the simple methods from the command line, 
        - integrate rocco's python inversion code