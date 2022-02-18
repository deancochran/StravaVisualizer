import os
import time
from django.urls import reverse
import numpy as np
import pandas as pd
import requests
from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import ArrayField
from datetime import datetime
import polyline

User = settings.AUTH_USER_MODEL

# Create your models here.

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_id = models.BigIntegerField(blank=True, null=True)
    achievement_count = models.IntegerField(blank=True, null=True)
    average_cadence = models.FloatField(blank=True, null=True)
    average_heartrate = models.FloatField(blank=True, null=True)
    average_speed = models.FloatField(blank=True, null=True)
    comment_count = models.IntegerField(blank=True, null=True)
    distance = models.FloatField(blank=True, null=True)
    elapsed_time = models.FloatField(blank=True, null=True)
    elevation_high = models.IntegerField(blank=True, null=True)
    elevation_low = models.IntegerField(blank=True, null=True)
    end_latlng = ArrayField(
        models.FloatField(blank=True, null=True),
        default=list, blank=True, null=True
    )

    kudo_count = models.IntegerField(blank=True, null=True)
    location_city = models.TextField(blank=True, null=True)
    location_state = models.TextField(blank=True, null=True)
    location_country = models.TextField(blank=True, null=True)
    # map_summary_polyline = models.TextField(blank=True, null=True)
    map_latitude = ArrayField(
        models.FloatField(blank=True, null=True),
        default=list, blank=True, null=True
    )
    map_longitude = ArrayField(
        models.FloatField(blank=True, null=True),
        default=list, blank=True, null=True
    )
    map_centroid = ArrayField(
        models.FloatField(blank=True, null=True),
        default=list, blank=True, null=True
    )
    map_elevation = ArrayField(
        models.FloatField(blank=True, null=True),
        default=list, blank=True, null=True
    )
    max_heartrate = models.FloatField(blank=True, null=True)
    max_speed = models.FloatField(blank=True, null=True)
    moving_time = models.FloatField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    photo_count = models.IntegerField(blank=True, null=True)
    pr_count = models.IntegerField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    start_date_local = models.DateTimeField(blank=True, null=True)
    start_latitude = models.FloatField(blank=True, null=True)
    start_longitude = models.FloatField(blank=True, null=True)
    start_latlng = ArrayField(
        models.FloatField(blank=True, null=True),
        default=list, blank=True, null=True
    )
    suffer_score = models.IntegerField(blank=True, null=True)
    timezone = models.TextField(max_length=2000, blank=True, null=True)
    total_elevation_gain = models.IntegerField(blank=True, null=True)
    type = models.TextField(max_length=2000, blank=True, null=True)
    utc_offset = models.BigIntegerField(blank=True, null=True)
    
    def has_latlng(self):
        if self.map_latitude is not None and self.map_longitude is not None:
            return True
        else:
            return False
    
    def get_globe_points(self):
        return {
            #points data
            'lat':float(self.start_latitude),
            'lng':float(self.start_longitude),
            'size': 1,
            'color': 'rgba(255,69,0,.3)'
        }

    def get_globe_paths(self):
        paths=[]
        for lat,lng in zip(self.map_latitude,self.map_longitude):
            paths.append([lat,lng,0])
        return {
            #paths data
            'paths' : paths,

            # label info
            'name':self.name,
            'type':self.type,
            'date': self.start_date_local.strftime('%Y-%M-%D %H:%M:%S'),
            'distance':float(self.distance),
            'elapsed_time':float(self.elapsed_time),
        }
    

def set_elevation(activity_id):
    activity = Activity.objects.get(id=activity_id)
    if activity.map_latitude is not None:
        elevation=[]
        locations=[]
        for coord in zip(activity.map_latitude,activity.map_longitude):
            # method 1
            # payload = str(coord[0])+','+str(coord[1])
            
            # method 2
            # payload = '['+str(coord[0])+','+str(coord[1])+']'

            # method 3
            payload = str(coord[0])+','+str(coord[1])
            locations.append(payload)
        # method 3

        n=512
        while len(locations) >=1:
            subset=locations[:n]
            del locations[:n]
            payloads="|".join(subset)
            print('downloading elevation data...')
            try:
                
                # method 1
                # r = requests.get('https://api.opentopodata.org/v1/srtm90m?locations='+payloads+'&interpolation=cubic',verify=True)

                # method 2
                # r = requests.get('https://elevation-api.io/api/elevation?points='+payloads+'&key=6Dk78ZeNad7f7Ra2-4aNy85yUxY020&resolution=30-interpolated',verify=True).json()

                # method 3
                r = requests.post('https://maps.googleapis.com/maps/api/elevation/json?locations='+payloads+'&key='+str(os.environ.get('GOOGLE_ELEVATION_API_KEY')))

                r=r.json()
                # print('gooood request')
            except:
                break
            
            print(r)
            # for result in r['elevations']:
            for result in r['results']:
                elevation.append(result['elevation'])
        if len(elevation) > 1:
            # print('saving request')
            activity.map_elevation =  elevation
            activity.save()
        else:
            print('bad request')
    else:
        print('map has not latlng data')
    




     

def get_polyline(polylineChars):
    if polylineChars is None:
        return None
    else:
        return polyline.decode(polylineChars)

def get_latlng(polyline):
    if polyline is not None:
        lats=[]
        longs=[]
        for coord in polyline:
            if coord is not None:
                lats.append(coord[0])
                longs.append(coord[1])
            else:
                lats.append(np.nan)
                longs.append(np.nan)
        return lats, longs
    else:
        return None, None

def getCentroid(lats, lngs):
    if lats is not None and lngs is not None:
        centroid = [
                np.mean(lats), 
                np.mean(lngs)   
            ]

        return centroid
    else:
        return None



def set_activity(user, activity_obj):
    a = Activity(user = user)
    a.activity_id = activity_obj['id']
    # a.achievement_count = activity_obj['achievement_count']
    # a.average_cadence = activity_obj['average_cadence']
    # a.average_heartrate = activity_obj['average_heartrate']
    # a.average_speed = activity_obj['average_speed']
    # a.comment_count = activity_obj['comment_count']
    a.distance = activity_obj['distance']
    a.elapsed_time = activity_obj['elapsed_time']
    a.elevation_high = activity_obj['elev_high']
    a.elevation_low = activity_obj['elev_low']
    a.end_latlng = activity_obj['end_latlng']
    # a.kudo_count = activity_obj['kudos_count']
    # a.location_city = activity_obj['location_city']
    # a.location_state = activity_obj['location_state']
    # a.location_country = activity_obj['location_country']
    # a.max_heartrate = activity_obj['max_heartrate']
    # a.max_speed = activity_obj['max_speed']
    a.moving_time = activity_obj['moving_time']
 
    a.name = activity_obj['name']
    # a.photo_count = activity_obj['photo_count']
    # a.pr_count = activity_obj['pr_count']
    a.start_date = activity_obj['start_date']
    a.start_date_local = activity_obj['start_date_local']
    a.start_latitude = activity_obj['start_latitude']
    a.start_longitude = activity_obj['start_longitude']
    a.start_latlng = activity_obj['start_latlng']
    
    # a.suffer_score = activity_obj['suffer_score']
    # a.timezone = activity_obj['timezone']
    # a.total_elevation_gain = activity_obj['total_elevation_gain']
    a.type = activity_obj['type']
    # a.utc_offset = activity_obj['utc_offset']
    polyline = get_polyline(activity_obj['map.summary_polyline'])

    a.map_latitude, a.map_longitude = get_latlng(polyline)
    if len(activity_obj['start_latlng']) != 0:
            a.map_centroid = getCentroid(a.map_latitude, a.map_longitude)
    
    a.save()


def set_activities(user, activities):
    # convert data types
    activities.loc[:, 'start_date'] = pd.to_datetime(activities['start_date']).dt.tz_localize(None)
    activities.loc[:, 'start_date_local'] = pd.to_datetime(activities['start_date_local']).dt.tz_localize(None)
    # convert values
    activities.loc[:, 'distance'] /= 1000 # convert from m to km
    activities.loc[:, 'average_speed'] *= 3.6 # convert from m/s to km/h
    activities.loc[:, 'max_speed'] *= 3.6 # convert from m/s to km/h
    activities.loc[:, 'elapsed_time'] /= 60 # convert from s to min

    
    activities = activities.astype(object).replace(np.nan, None)
    print('setting activities')
    for i, activity in activities.iterrows():
        if Activity.objects.filter(activity_id = activity['id']).exists() == False:
            set_activity(user, activity)

def get_new_activities(newData):
    for i, activity in newData.iterrows():
        if Activity.objects.filter(activity_id = activity['id']).exists() == True:
            newData = newData.drop(i)
    return newData