from hiking_trails_api_project.forms import NewUserForm, UserLoginForm
from hiking_trails_api.models import HikingTrails
from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.models import User
from folium.plugins import MarkerCluster, Fullscreen
from django.forms import ModelForm
from django.views.generic import (
  UpdateView
)
import pandas as pd
import folium


def maps(request):
  current_user = request.user
  df = pd.DataFrame(list(HikingTrails.objects.all().values()))
  print(df)
  map = folium.Map(zoom_start=7, location=df[["lat", "lon"]].astype(
    'float').mean().to_list())  # Starts zoom at average of lat/lon from pandas
  marker_cluster = MarkerCluster().add_to(map)  # Start a cluster to add to the map
  for i, r in df.iterrows():
    if current_user.id == r["owner_id"]:
      edit_button = f'''
        <a style="float: right" href="{r["id"]}/trail-update/" title="Edit Trail" target="_parent">
          <svg style="width: 20px" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-1 h-1">
            <path d="M5.433 13.917l1.262-3.155A4 4 0 017.58 9.42l6.92-6.918a2.121 2.121 0 013 3l-6.92 6.918c-.383.383-.84.685-1.343.886l-3.154 1.262a.5.5 0 01-.65-.65z" />
            <path d="M3.5 5.75c0-.69.56-1.25 1.25-1.25H10A.75.75 0 0010 3H4.75A2.75 2.75 0 002 5.75v9.5A2.75 2.75 0 004.75 18h9.5A2.75 2.75 0 0017 15.25V10a.75.75 0 00-1.5 0v5.25c0 .69-.56 1.25-1.25 1.25h-9.5c-.69 0-1.25-.56-1.25-1.25v-9.5z" />
          </svg
        </a>
                       </a>
        '''
    else:
      edit_button = ''

    html = f'''
        {edit_button}
        <h2 style="cursor: default" >{r["trail_name"].capitalize()}<h2/>
        <small  style="cursor: default">Added by <strong>{User.objects.get(id=r["owner_id"])}</strong> </small>
        <br>
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


class TrailUpdateForm(ModelForm):
  class Meta:
    model = HikingTrails
    fields = ["trail_name", "wta_link", "description"]

  trail_name = forms.CharField(disabled=True)
  wta_link = forms.CharField(disabled=True)


class TrailUpdateView(UpdateView):
  template_name = "trail_update.html"
  model = HikingTrails
  form_class = TrailUpdateForm


def documentation(request):
  context = dict(current_user=request.user)
  return render(request, 'documentation.html', context)


def hikers(request):
  context = dict(all_users=get_user_model().objects.all())
  context["current_user"] = request.user
  context["all_trails"] = HikingTrails.objects.all().order_by("trail_name")
  print(context["current_user"])
  return render(request, 'hikers.html', context)
