from django.urls import path
from . import views as vi 


app_name = 'waste'
urlpatterns = [  
    # pip install -U autopep8
    path('place-details/<int:place_id>',vi.view_place_details,name='place_details'), 
    path('waste-details',vi.view_waste_details,name='waste_details'), 
    path('waste-info/<int:waste_id>',vi.view_waste_info,name='waste_details'),
    path('add-waste/places',vi.add_place_to_cover,name='add_places'), 
    path('edit-waste/place/<int:location_id>',vi.edit_waste_places_covered,name='edit_place'), 
    path('delete-waste/place/<int:location_id>',vi.delete_waste_location_covered,name='delete_place'), 
    path('add-waste/type',vi.add_waste_type_collected,name='add_type'),
    path('edit-waste/type/<int:waste_id>',vi.edit_waste_type_collected,name='edit_type'), 
    path('delete-waste/type/<int:waste_id>',vi.delete_waste_type_collected,name='delete_type'), 
    path('wastes-disposed',vi.request_was_disposal,name='dispose_waste'), 
    path('view-sent/waste',vi.view_waste_sent,name='sent_waste'),
    path('check-waste/<int:bin_id>',vi.check_waste_bin,name='check_waste'),
    path('edit-waste/bin/<int:bin_id>',vi.edit_waste_bin,name='edit_bin'), 
    path('delete-waste/bin/<int:bin_id>',vi.delete_waste_bin,name='delete_bin'), 
    path('waste-settings',vi.add_waste_settings,name='waste_settings'),
    path('confirm-payment/<int:bin_id>',vi.confirm_payment,name='confirm_payment'),
    path('collect-dispose/<int:bin_id>',vi.collect_and_dispose,name='collected'),

]