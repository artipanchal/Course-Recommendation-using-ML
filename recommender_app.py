
import streamlit as st
import pandas as pd
import time
import backend as backend

from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid import GridUpdateMode, DataReturnMode


ALLOW_ANN = False

# Basic webpage setup
st.set_page_config(
   page_title="Course Recommender System",
   layout="wide",
   initial_sidebar_state="expanded",
)


# Load datasets
@st.cache
def load_ratings():
    """Load ratings dataframe: user, course, rating (2/3)."""
    return backend.load_ratings()

@st.cache
def load_course_sims():
    """Load course similarities dataframe: course vs. course."""
    return backend.load_course_sims()

@st.cache
def load_courses():
    """Load courses dataframe: course, title, description."""
    return backend.load_courses()

@st.cache
def load_bow():
    """Load course bags-of-words (BoW) descriptors:
    course index and name, token, bow-count."""
    return backend.load_bow()

@st.cache
def load_course_genres():
    """Load course genre table:
    course index, title, 14 binary genre features."""
    return backend.load_course_genres()

@st.cache
def load_user_profiles():
    """Load user profiles table:
    user id, 14 binary genre features."""
    return backend.load_user_profiles()

def init_recommender_app():
    """Initialization: It loads all dataframes to cache
    and builds and interactive AgGrid table for `course_processed.csv`
    from which user input is taken and used
    to generate a response dataframe.
    
    Inputs:
        None
    Outputs:
        results: pd.DataFrame
            Data frame with the selections by the user.
    """
    # Load all dataframes
    with st.spinner('Loading datasets...'):
       
        course_df = load_courses()
    
    st.success('Datasets loaded successfully...')
    st.markdown("""---""")
    st.subheader("Select courses that you have audited or completed: ")

    
    gb = GridOptionsBuilder.from_dataframe(course_df)
    gb.configure_default_column(enablePivot=True, enableValue=True, enableRowGroup=True)
    gb.configure_selection(selection_mode="multiple", use_checkbox=True)
    gb.configure_side_bar()
    grid_options = gb.build()

    # Create an AgGrid: an interactive table from which we get a response
    # with the rows selected by the user
    response = AgGrid(
        course_df,
        gridOptions=grid_options,
        enable_enterprise_modules=True,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        fit_columns_on_grid_load=False,
    )
    
    results = pd.DataFrame(response["selected_rows"],
                           columns=['COURSE_ID', 'TITLE', 'DESCRIPTION'])
    results = results[['COURSE_ID', 'TITLE']]
    st.subheader("Your courses: ")
    st.table(results)
    
    return results

@st.cache(suppress_st_warning=True)
def train(model_name, params):
    """Train function for
    the selected model + hyperparameters + courses.
    
    Inputs:
        model_name: str
            Model from the selectbox.
        params: dict
            Hyperparameters.
    Returns:
        training_artifacts: dict
            Any model-specific artifacts generated during training:
            pipelines, dataframes, etc.
    """
    training_artifacts = None
    try:
        assert model_name in backend.MODELS
        model_index = backend.get_model_index(model_selection)
        do_train = False
        if model_index > 5: # Neural Networks & Co.
            if ALLOW_ANN:
                do_train = True            
        else:
            do_train = True
        if do_train:  
            with st.spinner('Training...'):
                time.sleep(0.5)
                training_artifacts = backend.train(model_name, params)
            st.success('Done!')
        else:
            st.write("Sorry, the Neural Networks model is not active at the moment\
                due to the slug memory quota on Heroku. \
                If you clone the repository, \
                you can try it on your local machine, though.")
        return training_artifacts
    except AssertionError as err:
        print("Model name must be in the drop down.") # we should use the logger
        raise err

def predict(model_name, params, training_artifacts):
    """Predict function for
    the trained model.
    
    Inputs:
        model_name: str
            Model from the selectbox.
        user_ids: list
            User ids.
        params: dict
            Hyperparameters.
    Returns:
        res: pd.DataFrame
            Predicted/suggested courses.
    """
    res = None
    # Start making predictions based on model name, test user ids, and parameters
    try:
        assert model_name in backend.MODELS
        model_index = backend.get_model_index(model_selection)
        do_predict = False
        if model_index > 5: # Neural Networks & Co.
            if ALLOW_ANN:
                do_predict = True            
        else:
            do_predict = True
        if do_predict:
            with st.spinner('Generating course recommendations: '):
                time.sleep(0.5)
                
                new_id = params["new_id"]
                user_ids = [new_id]
                res, descr = backend.predict(model_name, user_ids, params, training_artifacts)
            st.success('Recommendations generated!')
            st.write(f"**{backend.MODELS[model_index][3:]}**: {backend.MODEL_DESCRIPTIONS[model_index]}")          
            st.write(descr)
        else:
            st.write("Sorry, the Neural Networks model is not active at the moment\
                due to the slug memory quota on Heroku. \
                If you clone the repository, \
                you can try it on your local machine, though.")
        return res
    except AssertionError as err:
        print("Model name must be in the drop down.") # we should use the logger
        raise err
        

st.sidebar.title('Personalized Learning Recommender')
selected_courses_df = init_recommender_app()




st.sidebar.subheader('1. Select recommendation models')
model_selection = st.sidebar.selectbox(
    "Select model:",
    backend.MODELS
)

params = {}
st.sidebar.subheader('2. Tune Hyper-parameters: ')
top_courses = st.sidebar.slider('Top courses',
                                min_value=1, max_value=100,
                                value=10, step=1)
params['top_courses'] = top_courses
# Model-dependent options
if model_selection == backend.MODELS[0]: # 0: "Course Similarity"
    course_sim_threshold = st.sidebar.slider('Course similarity threshold %',
                                             min_value=0, max_value=100,
                                             value=50, step=10)
    params['sim_threshold'] = course_sim_threshold
elif model_selection == backend.MODELS[1]: # 1: "User Profile"
    profile_threshold = st.sidebar.slider('Course topic alignment score',
                                          min_value=0, max_value=100,
                                          value=1, step=1)
    params['profile_threshold'] = profile_threshold
elif model_selection == backend.MODELS[2]: # 2: "Clustering"
    num_clusters = st.sidebar.slider('Number of clusters',
                                   min_value=1, max_value=30,
                                   value=11, step=1)
    params['num_clusters'] = num_clusters
    params['pca_variance'] = 1.0
elif model_selection == backend.MODELS[3]: # 3: "Clustering with PCA"
    num_clusters = st.sidebar.slider('Number of clusters',
                                   min_value=1, max_value=30,
                                   value=11, step=1)
    pca_variance = st.sidebar.slider('Genre variance coverage (PCA)',
                                   min_value=0, max_value=100,
                                   value=90, step=5)
    params['num_clusters'] = num_clusters
    params['pca_variance'] = pca_variance / 100.0
elif model_selection == backend.MODELS[4]: # 4: "KNN"
    pass
elif model_selection == backend.MODELS[5]: # 5: "NMF"
    num_components = st.sidebar.slider('Number of latent components (discovered topics)',
                                   min_value=1, max_value=30,
                                   value=15, step=1)
    params['num_components'] = num_components
elif model_selection == backend.MODELS[6] \
    or model_selection == backend.MODELS[7]\
    or model_selection == backend.MODELS[8]: # 6: "Neural Network"
    num_components = st.sidebar.slider('Number of latent components (embedding size)',
                                   min_value=1, max_value=30,
                                   value=16, step=1)
    num_epochs = st.sidebar.slider('Number of epochs',
                                   min_value=1, max_value=100,
                                   value=1, step=1)
    params['num_components'] = num_components
    params['num_epochs'] = num_epochs
    
    
    if model_selection == backend.MODELS[7]: # 7: "Regression with Embedding Features"
        pass
    elif model_selection == backend.MODELS[8]: # 8: "Classification with Embedding Features"
        pass


st.sidebar.subheader('3. Training: ')
training_button = False
training_button = st.sidebar.button("Train Model")
training_text = st.sidebar.text('')

training_artifacts = None
model_index = backend.get_model_index(model_selection)

if training_button and model_index < 6:
   
    training_artifacts = train(model_selection, params)


st.sidebar.subheader('4. Prediction')
pred_button = st.sidebar.button("Recommend New Courses")
if pred_button and selected_courses_df.shape[0] > 0:
    if model_index < 6 and not training_artifacts:
        

        training_artifacts = train(model_selection, params)
    
    new_id = backend.add_new_ratings(selected_courses_df['COURSE_ID'].values)
    params["new_id"] = new_id
    if model_index > 5:
        
        training_artifacts = train(model_selection, params)
    if new_id:
        res_df = predict(model_selection, params, training_artifacts)
        if not res_df.empty:
         res_df = res_df[['COURSE_ID', 'SCORE']]
        else:
         print("The DataFrame is empty. Cannot select columns.")

        course_df = load_courses()
        res_df = pd.merge(res_df, course_df, on=["COURSE_ID"]).drop('COURSE_ID', axis=1)
        st.table(res_df)
