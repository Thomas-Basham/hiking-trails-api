from django.shortcuts import render, redirect
from django_pandas.io import read_frame
from hiking_trails_api_project.forms import NewUserForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
import folium
from folium.plugins import MarkerCluster, Fullscreen
from django.forms import ModelForm
from hiking_trails_api.models import HikingTrails


def maps(request):
    current_user = request.user
    df = read_frame(HikingTrails.objects.all())
    map = folium.Map(zoom_start=7, location=df[["lat", "lon"]].astype('float').mean().to_list() )

    marker_cluster = MarkerCluster().add_to(map)
    for i, r in df.iterrows():
        html = f'''
        <h2 >{r["trail_name"].capitalize()}<h2/>
        <a style="color:blue" href="{r["google_maps_directions"]}" target="_blank">Directions via Googlemaps <a/>
        <br>
        <a style="color:green" href="{r["all_trails_link"]}" target="_blank">Link to All-Trails site<a/>
        <p >{r["description"]}<p/>
        '''
        iframe = folium.IFrame(html, width=200, height=300)
        popup = folium.Popup(iframe)

        location = (r["lat"], r["lon"])

        folium.Marker(location=location, tooltip=r["trail_name"].capitalize(), popup=popup).add_to(
            marker_cluster)

    folium.raster_layers.TileLayer('Stamen Terrain').add_to(map)
    folium.raster_layers.TileLayer('Stamen Watercolor').add_to(map)
    folium.LayerControl().add_to(map)
    Fullscreen(
        position='topright',
        title='Expand me',
        title_cancel='Exit me',
        force_separate_button=True
    ).add_to(map)
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
            messages.success(request, "Registration successful.")
            return redirect("login")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
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
    form = AuthenticationForm()
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
        form = AddTrailForm(request.POST, request.FILES)
        context['posted'] = form.instance
        if form.is_valid():
            form.save()
        return redirect('maps')

    return render(request, 'add_trail_form.html', context)


class AddTrailForm(ModelForm):
    class Meta:
        model = HikingTrails
        fields = "__all__"
