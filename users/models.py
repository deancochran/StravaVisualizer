from datetime import timedelta
import os
from PIL import Image
from django.utils import timezone
import json 
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from pandas import json_normalize
import requests
from activities.models import Activity, set_activities, get_new_activities
from users.utils import form_landscape_img, form_routes_img


class User(AbstractUser):
    access_token = models.CharField(max_length=100, blank=True, default=None, null=True)
    refresh_token = models.CharField(max_length=100, blank=True, default=None, null=True)
    expires_in = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    last_authenticated = models.DateTimeField(blank=True, null=True)
    athlete_id = models.IntegerField(blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    profile_image = models.ImageField(upload_to='images/',default='default.jpg')

    
    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def get_absolute_landscape_url(self):
        return reverse("users:landscapes", kwargs={"username": self.username})

    def get_absolute_routes_url(self):
        return reverse("users:routes", kwargs={"username": self.username})


    
    def has_activities(self):
        if Activity.objects.filter(user = self.id).exists():
            return True
        else:
            return False


    def download_activities(self, only_new_activities=False):
        print('downloading activities from strava.com')
        #Loop through all activities
        page = 1
        data = list()
        while True:
            # get page of activities from Strava
            urlActivities = "https://www.strava.com/api/v3/activities"
            #r = requests('GET',urlActivities + '?access_token=' + access_token + '&per_page=200' + '&page=' + str(page))
            r = requests.get(urlActivities + '?access_token=' + self.access_token + '&per_page=200' + '&page=' + str(page)).json()
            # if no results then exit loop
            if (not r):
                break
            data.append(r)
            page += 1# Export your activities file as a csv 
        # data dictionaries
        data_dictionaries = []
        for page in data:
            data_dictionaries.extend(page)
        # print number of activities
        print('Number of activities downloaded: {}'.format(len(data_dictionaries)))
        if only_new_activities:
            print('user has', len(Activity.objects.filter(user = self.id)), 'activities')
            print('looking for new activities')
            if len(data_dictionaries) > len(self.get_activities()):
                set_activities(self,get_new_activities(json_normalize(data_dictionaries)))
                print('set new activities')
                
            else:
                print('did not set new activities')
                
        else:
            print('user has', len(Activity.objects.filter(user = self.id)), 'activities')
            print('first time setting activities')
            set_activities(self,json_normalize(data_dictionaries))

    
    def get_activities(self, missing_elevations=False):
        
        if  missing_elevations == True:
            subset=[]
            for activity in Activity.objects.filter(user = self.id):
                if len(activity.map_elevation)<1  and activity.map_latitude is not None:
                    subset.append(activity)
            return subset
        else:
            return Activity.objects.filter(user = self.id)

    def get_num_activities_for_elevation(self):
        container=[]
        for a in self.get_activities():
            if a.has_latlng():
                container.append(a)
        return len(container)

    def get_landscapes_img(self):
        print('maden it to the landscapes image function in user models')
        img = Image.new('RGB', (100, 100), (255,255,255))
        subset=[]
        for activity in Activity.objects.filter(user = self.id):
            if activity.map_longitude is not None and activity.map_latitude is not None and len(activity.map_elevation) > 1:
                subset.append(activity)
        
        new_img = form_landscape_img(subset)
        return new_img

    def get_routes_img(self):
        print('maden it to the routes image function in user models')
        img = Image.new('RGB', (100, 100), (255,255,255))
        subset=[]
        for activity in Activity.objects.filter(user = self.id):
            if activity.map_longitude is not None and activity.map_latitude is not None and len(activity.map_elevation) > 1:
                subset.append(activity)
        
        new_img = form_routes_img(subset)
        return new_img


    def has_access(self,request):
        print('checking acess from strava.com')
        print('validating code and json response')
        code = request.GET.get('code')
        self.last_authenticated = timezone.now()
        clientID=os.environ.get('CLIENT_ID')
        clientSECRET=os.environ.get('CLIENT_SECRET')
        data = {
            'client_id': clientID,
            'client_secret': clientSECRET,                                 
            'code': code,
            'grant_type': 'authorization_code'
        }
        url = 'https://www.strava.com/api/v3/oauth/token'
        response = requests.post(url = url,data = data)
        response = response.json()
        print(response)
        if 'errors' in response.keys():
            print('invalid json response')
            return False
        else:
            print('valid json response')
            self.access_token = response['access_token']
            self.refresh_token = response['refresh_token']
            self.expires_at = add_sec_to_dt_now(response['expires_at'])
            self.expires_in = add_sec_to_dt_now(response['expires_in'])
            athlete = response['athlete']
            self.athlete_id = athlete['id']
            self.bio = athlete['bio']
            self.profile_image = athlete['profile']
            self.save()
            return True
            

    def update_access(self):
        print('updating access from strava.com')
        print('self.expires_at,',self.expires_at)
        print('self.expires_in,',self.expires_in)
        print('updating access, likely a refresh or myprofile page call')
        if timezone.now() > self.expires_at:
            print('user refresh expired... unsolved issue')
        else:
            if timezone.now() > self.expires_in:
                print('access is expired')
                clientID=os.environ.get('CLIENT_ID')
                clientSECRET=os.environ.get('CLIENT_SECRET')
                data = {
                    'client_id': clientID,
                    'client_secret': clientSECRET,                                 
                    'refresh_token': self.refresh_token,
                    'grant_type': 'refresh_token'
                }
                url = 'https://www.strava.com/api/v3/oauth/token'
                response = requests.post(url = url,data = data)
                response = response.json()
                print(response)
                self.access_token = response['access_token']
                self.refresh_token = response['refresh_token']
                self.expires_at = add_sec_to_dt_now(response['expires_at'])
                self.expires_in = add_sec_to_dt_now(response['expires_in'])
            else:
                print('access is not expired... user likes to click and refresh')

    def get_globeData(self):
        activities=Activity.objects.filter(user = self.id)
        globeData={
            'pointsData':[],
            'pathsData':[]
        }
        for activity in activities:
            if activity.has_latlng():
                points = activity.get_globe_points()
                paths = activity.get_globe_paths()
                globeData['pointsData'].append(points)
                globeData['pathsData'].append(paths)
        return json.dumps(globeData)

            
def add_sec_to_dt_now(seconds):
    print('converting expire times to future DT')
    time_change = timedelta(seconds=seconds)
    return timezone.now() + time_change