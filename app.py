import streamlit as st
import pickle
import pandas as pd
# CSS for full-page background image
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://www.debongo.com/wp-content/uploads/2020/10/IPL-History-Price-Money-and-Passion-behind-It-Debongo.png");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }
    </style>
""", unsafe_allow_html=True)
teams = ['Sunrisers Hyderabad',
         'Mumbai Indians',
         'Royal Challengers Bangalore',
         'Kolkata Knight Riders',
         'Kings XI Punjab',
         'Chennai Super Kings',
         'Rajasthan Royals',
         'Delhi Capitals']

cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
          'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
          'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
          'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
          'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
          'Sharjah', 'Mohali', 'Bengaluru']

# Load the trained model pipeline
pipe = pickle.load(open('pipe.pkl', 'rb'))

st.title('IPL Win Predictor')
col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select the batting team', sorted(teams))
with col2:
    bowling_team = st.selectbox('Select the bowling team', sorted(teams))

selected_city = st.selectbox('Select host city', sorted(cities))

target = st.number_input('Target', min_value=0, step=1)

col3, col4, col5 = st.columns(3)
with col3:
    score = st.number_input('Score', min_value=0, step=1)
with col4:
    overs = st.number_input('Overs completed', min_value=0.0, step=0.1, format="%.1f")
with col5:
    wickets = st.number_input('Wickets out', min_value=0, max_value=10, step=1)

if st.button('Predict Probability'):
    if overs == 0:
        st.error("Overs completed cannot be zero.")
    else:
        runs_left = target - score
        balls_left = max(0, int(120 - (overs * 6)))
        wickets_left = 10 - wickets
        crr = score / overs  # current run rate
        rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0  # required run rate

        input_df = pd.DataFrame({
            'batting_team': [batting_team],
            'bowling_team': [bowling_team],
            'city': [selected_city],
            'runs_left': [runs_left],
            'balls_left': [balls_left],
            'wickets': [wickets_left],
            'total_runs_x': [target],
            'crr': [crr],
            'rrr': [rrr]
        })

        result = pipe.predict_proba(input_df)
        loss = result[0][0]
        win = result[0][1]

        st.header(f"{batting_team} - {round(win * 100)}%")
        st.header(f"{bowling_team} - {round(loss * 100)}%")
