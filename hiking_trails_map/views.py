from django.shortcuts import render, redirect
from django_pandas.io import read_frame
from hiking_trails_api_project.forms import NewUserForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
import folium
from folium.plugins import MarkerCluster, Fullscreen
from django.forms import ModelForm
from hiking_trails_api.models import HikingTrails
from django.contrib.auth import get_user_model
from django.views.generic import (
    UpdateView,
)

def maps(request):
    current_user = request.user
    df = read_frame(HikingTrails.objects.all())
    map = folium.Map(zoom_start=7, location=df[["lat", "lon"]].astype(
        'float').mean().to_list())  # Starts zoom at average of lat/lon from pandas
    marker_cluster = MarkerCluster().add_to(map)  # Start a cluster to add to

    for i, r in df.iterrows():
        html = f'''
        <h2 >{r["trail_name"].capitalize()}<h2/>
        <a style="color:blue" href="{r["google_maps_directions"]}" target="_blank" rel="nofollow" >Directions via Googlemaps <a/>
        <br>
        <a style="color:green" href="{r["wta_link"]}" target="_blank">Link to WTA Page<a/>
        <p >{r["description"]}<p/>
        '''
        popup = folium.Popup(html, max_width=500)

        location = (r["lat"], r["lon"])

        folium.Marker(location=location, tooltip=r["trail_name"].capitalize(), popup=popup,
                      ).add_to(marker_cluster)

    Fullscreen(
        position='topright',
        title='Expand me',
        title_cancel='Exit me',
        force_separate_button=True
    ).add_to(map)

    folium.raster_layers.TileLayer('Stamen Terrain').add_to(map)
    folium.raster_layers.TileLayer('Stamen Watercolor').add_to(map)
    folium.LayerControl().add_to(map)

    map = map._repr_html_()

    context = {
        'map': map,
        'current_user': current_user,
        'add_trail_form': AddTrailForm()
    }

    return render(request, 'hiking_trails_map.html', context)


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Registration successful. logged in as {request.user} ")
            return redirect("maps")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            username = username.lower()
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("maps")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = UserLoginForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("maps")


def add_trail_form(request):
    context = dict(add_trail_form=AddTrailForm())
    context["dataset"] = HikingTrails.objects.all().order_by("-id")
    context["current_user"] = request.user
    if request.method == 'POST':
        form = AddTrailForm(request.POST)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.owner = request.user
            stock.save()
        return redirect('maps')

    return render(request, 'add_trail_form.html', context)


class AddTrailForm(ModelForm):
    class Meta:
        model = HikingTrails
        fields = ["wta_link", "description"]
        labels = {"wta_link": "WTA Link"}
        help_texts = {"wta_link": "Ex: https://www.wta.org/go-hiking/hikes/talapus-and-olallie-lakes "}


class HikingTrailUpdateView(UpdateView):
    template_name = "trail_update.html"
    model = HikingTrails
    fields = ['description']

def documentation(request):
    context = dict(current_user=request.user)
    return render(request, 'documentation.html', context)


def hikers(request):
    context = dict(all_users=get_user_model().objects.all())
    context["all_trails"] = HikingTrails.objects.all().order_by("trail_name")

    return render(request, 'hikers.html', context)
