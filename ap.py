#Importing GEE Requirements

import ee
ee.Initialize()
from IPython.display import Image,display
import folium
import json
import os
import requests
import pygeoj
from flask import Flask, render_template, request, send_file
from PIL import Image
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('map.html')

@app.route("/", methods=["POST"])
def getvalue():
    start_date = request.form['st_date']
    end_date = request.form['ed_date']
    img = request.form['imagery']
    roi = request.form['roi']
    data = request.form['data']
    
    a = pygeoj.load(roi)
    for feature in a:
        roi = (feature.geometry.coordinates)
    region = ee.Geometry.MultiPolygon(roi)
    
    def index_calculation(a,b):
        return a.subtract(b).divide(a.add(b))
    
    
    def ndvi(img , region , start_date , end_date):
        data = ee.ImageCollection(img).filterBounds(region).filterDate(start_date,end_date).median()
        vis_params = {"min": -1, "max": 1, "palette": ['blue', 'white', 'green']}
        
        if (img == "LANDSAT/LC08/C01/T1_RT"):
            data = ee.ImageCollection(img).filterBounds(region).filterDate(start_date,end_date).sort('CLOUD_COVER').first()
            nir = data.select('B5')
            red = data.select('B4')
            data = index_calculation(nir,red)
            # vis_params = {"min": -1, "max": 1, "palette": ['blue', 'white', 'green']}
          
        elif (img == "COPERNICUS/S2_SR"):
            nir = data.select('B8')
            red = data.select('B4')
            data = index_calculation(nir,red) 
            # vis_params= {"opacity":1,"bands":["B8"],"min":0.20868456628048035,"max":0.33335007464955435,"palette":["04ff00","ffc800"]}
            
        data=data.clip(region)
        # url = data.getThumbUrl({"dimensions":1000,"opacity":1})
        # img = Image(url)
        map_id_dict = ee.Image(data).getMapId(vis_params)
        
        tile = str(map_id_dict['tile_fetcher'].url_format)
        
        return tile

    def ndbi(img , region , start_date , end_date):
        data = ee.ImageCollection(img).filterBounds(region).filterDate(start_date,end_date).median()
        vis_params = {"min": -1, "max": 1, "palette": ['ec5e08','e5bd09','8af204', '3ae204']}
        
        if (img == "LANDSAT/LC08/C01/T1_RT"):
            data = ee.ImageCollection(img).filterBounds(region).filterDate(start_date,end_date).sort('CLOUD_COVER').first()
            data = data.clip(region)
            swir1 = data.select('B6')
            nir = data.select('B5')
            data = index_calculation(swir1,nir)
            # vis_params = {"opacity":1,"bands":["B6"],"min":-0.4212116988711605,"max":-0.12628187297607416,"palette":["ff7600","fff700","1bff00"]}
        elif (img == "COPERNICUS/S2_SR"):
            swir1 = data.select('B11')
            data = data.clip(region)
            nir = data.select('B8')
            data = index_calculation(swir1,nir)
            # vis_params = {"opacity":1,"bands":["B12"],"min":-0.6638634079736231,"max":0.27875025492150074,"palette":["00ff66","fbff00","ffc800"]}; 
            

        map_id_dict = ee.Image(data).getMapId(vis_params)
        
        tile = str(map_id_dict['tile_fetcher'].url_format)
        
        return tile
    
    def ndwi(img , region , start_date , end_date):
        data = ee.ImageCollection(img).filterBounds(region).filterDate(start_date,end_date).median()
        
        vis_params = {"min": -1, "max": 1, "palette": ['blue','white', 'green']}
        
        if (img == "LANDSAT/LC08/C01/T1_RT"):
            data = ee.ImageCollection(img).filterBounds(region).filterDate(start_date,end_date).sort('CLOUD_COVER').first()
            nir = data.select('B5')
            swir1 = data.select('B6')
            data = index_calculation(swir1,nir)
        elif (img == "COPERNICUS/S2_SR"):
            nir = data.select('B8')
            swir1 = data.select('B11')
            data = index_calculation(swir1,nir) 
        
        data = data.clip(region)
            
        map_id_dict = ee.Image(data).getMapId(vis_params)
        
        tile = str(map_id_dict['tile_fetcher'].url_format)
        
        return tile
    
    def hillshade(img , region , start_date , end_date):
        data = ee.Image("USGS/SRTMGL1_003")
        dem = data.clip(region)
        hillshade = ee.Terrain.hillshade(dem)
        
        vis_params = {"opacity":1}
        
        map_id_dict = ee.Image(hillshade).getMapId(vis_params)
        
        tile = str(map_id_dict['tile_fetcher'].url_format)
        
        return tile        
    
    def slope(img , region , start_date , end_date):
        data = ee.Image("USGS/SRTMGL1_003")
        dem = data.clip(region)
        slope = ee.Terrain.slope(dem)
        
        vis_params = {"opacity":1}
        
        map_id_dict = ee.Image(slope).getMapId(vis_params)
        
        tile = str(map_id_dict['tile_fetcher'].url_format)
        
        return tile
    
    def aspect(img , region , start_date , end_date):
        data = ee.Image("USGS/SRTMGL1_003")
        dem = data.clip(region)
        aspect = ee.Terrain.aspect(dem)
        
        vis_params = {"opacity":1}
        
        map_id_dict = ee.Image(aspect).getMapId(vis_params)
        
        tile = str(map_id_dict['tile_fetcher'].url_format)
        
        return tile
        
    
    
    if (data=='ndvi'):
        data = ndvi(img , region , start_date , end_date)
    elif (data=='ndbi'):
        data = ndbi(img , region , start_date , end_date)
    elif (data=='ndwi'):
        data= ndwi(img , region , start_date , end_date)
    elif(data=='hillshade'):
        data= hillshade(img , region , start_date , end_date)
    elif(data=='slope'):
        data = slope(img , region , start_date , end_date)
    elif(data=='aspect'):
        data = aspect(img , region , start_date , end_date)
    elif(imagery_path == 'USGS/SRTMGL1_003'):
        data = dem(img , region , start_date , end_date)
    


    # image = Image.open('files/images/template.jpg')
    # map1 = Image(data)
    # new_height = int(map1.width*3431/1773)
    # new_width = int(map1.height*3431/1773) 

    # map2 = map1.resize((new_width,new_height),Image.ANTIALIAS)
    # image_copy = image.copy()

    # position = ((1715-(map2.width//2)),(1150-(map2.height//2)))
    # image_copy.paste(map2,position)
    # image_copy.save('abc2.jpg')
    # image_copy.show()

    return render_template('map.html', tiles=data)
    

if __name__ == "__main__":
    app.run(debug=True  )
    