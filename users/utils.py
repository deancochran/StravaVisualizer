import io
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
import seaborn as sns
sns.set()
from django.templatetags.static import static
Image.MAX_IMAGE_PIXELS = None


def form_landscape_img(activities):

    plt.figure(figsize=(20,30))
    for activity in activities:
        activity.map_elevation = [0 if x is None else x for x in activity.map_elevation]
        min_val = min(activity.map_elevation)
        max_val = max(activity.map_elevation)
        # print('activity:', activity.name)
        Y = []
        for x in activity.map_elevation:
            try:
                result= (x - min_val) / (max_val - min_val) 
            except:
                result = 0
            Y.append(result)
        Y = gaussian_filter1d(Y, sigma=3)
        X=np.linspace(0,1,len(Y))
        plt.fill_between(X, Y, color = 'black', alpha = 0.03, linewidth = 0)
        plt.plot(X,Y, color = 'black', alpha = 0.3, linewidth = 0.1)

    plt.axis('off')
    plt.margins(0)
    plt.subplots_adjust(left = 0.05, right = 0.95, bottom = 0.05, top = 0.95)
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png', dpi=800)

    bg = Image.open(img_buf).convert("RGBA")
    # fg = Image.open('static/images/sm-logo-icon.png').convert("RGBA")
    # bg.paste(fg, (0, 0), fg)

    return bg
        

def form_routes_img(activities):

    n = len(activities)
    nrow = 3
    ncol = 2
    while nrow*ncol < n:
        nrow+=3
        ncol+=2
    fig, axs = plt.subplots(nrows=nrow, ncols=ncol,figsize=(20,30), subplot_kw=dict(projection='3d'))
    plt.subplots_adjust(wspace=0, hspace=0)
    fig.set_facecolor('white')

    activity_index=0
    for ax in axs.reshape(-1):
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.patch.set_alpha(0.01)
        ax.axis('off')
        ax.grid(False)  

        try:
            # activity = activitiesMapped.iloc[activity_index, :] # first activity (most recent)
            activity = activities[activity_index] # first activity (most recent)
            activity_index+=1
            xs=activity.map_latitude
            ys=activity.map_longitude
            zs=range(len(activity.map_longitude))
            # ax.plot(xs, ys, zs, zdir='z', c = 'black')
            ax.scatter3D(xs, ys, zs, c=zs)
        except:
            pass
            
    plt.tight_layout(pad=0)
    plt.axis('off')
    plt.margins(0)
    plt.subplots_adjust(left = 0.05, right = 0.95, bottom = 0.05, top = 0.95)
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png', dpi=800)

    bg = Image.open(img_buf).convert("RGBA")
    fg = Image.open('static/images/routes-logo-icon-text.png').convert("RGBA")
    fg_width=fg.size[0]
    fg_height=fg.size[1]
    bg_width=bg.size[0]
    bg_height=bg.size[1]
    head_center=(int(bg_width//4),int(bg_height-(fg_height*2)))
    bg.paste(fg, head_center, mask=fg)

    return bg
        