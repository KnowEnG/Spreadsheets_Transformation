"""
Copyright 2017 University of Illinois Board of Trustees. All Rights Reserved.
Licensed under the MIT  license (the "License");
You may not use this file except in compliance with the License.
The License is included in the distribution as License.txt file.
 
Software  distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and  limitations under the License.
"""
import time
import numpy as np

import matplotlib.pyplot as plt

from   IPython.display import clear_output
from   lifelines import KaplanMeierFitter
from   lifelines.statistics import multivariate_logrank_test

from   knpackage import toolbox as kn

import sys
from   .layout_notebooks import *

RESOLUTION = 100
IM_SIZE = (12, 8)
plt.rcParams["figure.figsize"] = IM_SIZE

BLAK_IMAGE = bytes(np.zeros((IM_SIZE[0] * 4, IM_SIZE[1] * 4)))

results_dir = USER_RESULTS_DIRECTORY
input_data_dir = USER_DATA_DIRECTORY

DEFAULT_DATA_FILE = 'Kaplan_Meijer_data.tsv'
DEFAULT_OUTPUT_FILE_NAME = 'Kaplan_Meier_Plot.png'

# remove clutter - messages from lifelines:
clear_output()

""" make the controls - the first shows the list of phenotype ids COUPLED TO the phenotype file selection """
cluster_id_listbox          = widgets.Dropdown(options=[''], value='', description='Cluster_ID')
event_id_listbox            = widgets.Dropdown(options=[''], value='', description='event')
time_id_listbox             = widgets.Dropdown(options=[''], value='', description='time')

get_km_file_button          = get_select_view_file_button_set(input_data_dir)


def reset_phenotype_cols_list(change):
    """ Reset the three parameters dropdown listboxes to a new file selection.
    Args:
        change:      IPywidgets widget control change event
    """
    if get_km_file_button.file_selector.value == LIST_BOX_UPDATE_MESSAGE:
        if get_km_file_button.description == 'Clear':
            get_km_file_button.view_box.value = ''
            get_km_file_button.view_box.description = ''
            get_km_file_button.description = 'View'
        refresh_files_list(get_km_file_button)

        return
    options_df = kn.get_spreadsheet_df(os.path.join(input_data_dir, get_km_file_button.file_selector.value))
    sorted_options_list = sorted(list(options_df.columns.values))
    if len(sorted_options_list) > 0:
        def_val = sorted_options_list[0]
    else:
        def_val = ''
    cluster_id_listbox.options = sorted_options_list
    cluster_id_listbox.value = def_val
    event_id_listbox.options = sorted_options_list
    event_id_listbox.value = def_val
    time_id_listbox.options = sorted_options_list
    time_id_listbox.value = def_val

get_km_file_button.file_selector.observe(reset_phenotype_cols_list, names='value')


def disp_kaplan_meier(phenotype_df, cluster_id_name, event_name, time_name, button):
    """ display and save the output graphic """    
    T = phenotype_df[time_name]
    C = phenotype_df[event_name]
    
    results = multivariate_logrank_test(T, phenotype_df[cluster_id_name], C, alpha=0.99)
    button.view_box.value = str('multivariate_logrank_test; p_value = %g'%(results.p_value))
    
    Clusters     = sorted(phenotype_df[cluster_id_name].unique())
    num_clusters = len(Clusters)

    plt.clf()
    ax     = plt.subplot(111)

    kmf = KaplanMeierFitter()
    for cluster in Clusters:
        ixc = phenotype_df[cluster_id_name] == cluster
        kmf.fit ( T.ix[ixc], C.ix[ixc]         , label=cluster+1 )
        kmf.plot( ax=ax    , show_censors=True, ci_show=False    )

    plt.title ('number of clusters = %s' %(num_clusters))
    plt.xlabel('Time (days)'                            )
    plt.ylabel('OS'                                     )
    
    im_filename = os.path.join(results_dir, DEFAULT_OUTPUT_FILE_NAME)
    if os.path.isfile(im_filename) == True:
        os.remove(im_filename)

    plt.savefig(im_filename, dpi=100)
    
    count = 0
    max_count = 1000
    delay_time = 10.0 / max_count
    while os.path.isfile(im_filename) == False and count < max_count:
        count += 1
        time.sleep(delay_time)
    
    with open(im_filename, "rb") as file_handle:
        button.im_view_box.value = file_handle.read()
    
    
def run_kaplan_meier(button):
    """ callback for kaplan_meier_execute_button """
    if get_km_file_button.file_selector.value == LIST_BOX_UPDATE_MESSAGE:
        if get_km_file_button.description == 'Clear':
            get_km_file_button.view_box.value = ''
            get_km_file_button.view_box.description = ''
            get_km_file_button.description = 'View'
        refresh_files_list(get_km_file_button)
        
        return
    
    if button.description == 'Clear':
        button.description = button.original_description
        button.im_view_box.value = BLAK_IMAGE
        button.view_box.value = ''
        return
    else:
        button.description = 'Clear'
        
    phenotype_df = kn.get_spreadsheet_df(os.path.join(input_data_dir, get_km_file_button.file_selector.value))
    cluster_id_name = button.cluster_id_listbox.value
    event_name = button.event_id_listbox.value
    time_name = button.time_id_listbox.value

    disp_kaplan_meier(phenotype_df, cluster_id_name, event_name, time_name, button)


def get_kaplan_meier_execute_button():
    kaplan_meier_execute_button     = get_single_file_execute_button(
                                        input_data_dir, 
                                        results_dir, 
                                        file_selector=get_km_file_button.file_selector, 
                                        button_name='Plot',
                                        )
    kaplan_meier_execute_button.original_description = kaplan_meier_execute_button.description
    kaplan_meier_execute_button.view_box = get_view_box()
    kaplan_meier_execute_button.im_view_box = widgets.Image(value=BLAK_IMAGE, format='png')
    kaplan_meier_execute_button.im_view_box.value = BLAK_IMAGE

    kaplan_meier_execute_button.cluster_id_listbox = cluster_id_listbox
    kaplan_meier_execute_button.event_id_listbox = event_id_listbox
    kaplan_meier_execute_button.time_id_listbox = time_id_listbox

    if os.path.isfile(os.path.join(input_data_dir, DEFAULT_DATA_FILE)):
        get_km_file_button.file_selector.value = DEFAULT_DATA_FILE
        reset_phenotype_cols_list('de nada')
        kaplan_meier_execute_button.cluster_id_listbox.value = 'ClusterID'
        kaplan_meier_execute_button.event_id_listbox.value = 'event'
        kaplan_meier_execute_button.time_id_listbox.value = 'time'

    kaplan_meier_execute_button.on_click(run_kaplan_meier)
    return kaplan_meier_execute_button

def show_Kaplan_Meier_execute_button(button):
    """ show one button on the right with an ouput view box below """
    display(widgets.HBox([button], layout=right_buttons_style_box_layout))
    display(button.view_box)
    display(button.im_view_box)

def display_kaplan_meier_controls():
    # display control widgets
    show_select_view_button(get_km_file_button)
    show_widget_left(widgets.VBox([cluster_id_listbox,
                             event_id_listbox,
                             time_id_listbox,
                            ]))
    show_Kaplan_Meier_execute_button(get_kaplan_meier_execute_button())

