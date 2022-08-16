from django.urls import path
from . import views as vi 


app_name = 'waste'
urlpatterns = [  
    # path('waste-places',vi.places_covered,name='waste_locations'), 
    path('add-waste/places',vi.add_place_to_cover,name='add_places'), 
    path('edit-waste/place/<int:location_id>',vi.edit_waste_places_covered,name='edit_place'), 
    path('delete-waste/place/<int:location_id>',vi.delete_waste_location_covered,name='delete_place'), 
    path('add-waste/type',vi.add_waste_type_collected,name='add_type'),
    path('edit-waste/type/<int:waste_id>',vi.edit_waste_type_collected,name='edit_type'), 
    path('delete-waste/type/<int:waste_id>',vi.delete_waste_type_collected,name='delete_type'), 
    path('wastes-disposed',vi.request_was_disposal,name='dispose_waste'), 
    path('edit-waste/bin/<int:bin_id>',vi.edit_waste_bin,name='edit_bin'), 
    path('delete-waste/bin/<int:bin_id>',vi.delete_waste_bin,name='delete_bin'), 
    path('waste-settings',vi.add_waste_settings,name='waste_settings')
]