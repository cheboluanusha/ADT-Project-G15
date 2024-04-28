import mysql.connector
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Connect to MySQL
conn = mysql.connector.connect(
    host="sh4ob67ph9l80v61.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",
    user="udq91g1s9azjkmg4",
    password="nd3x0izhjouy74x0",
    database="lg6w0pwczcwa1hnj"
)

# Create a Streamlit app
st.title('Fortnite Player Data')

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the image file
image_filename = "fortnite.jpg"
image_path = os.path.join(current_dir, image_filename)

# Display the image on the right side
st.image(image_path, use_column_width=True)

# Initialize user session
session_state = st.session_state
if 'logged_in' not in session_state:
    session_state.logged_in = False
    session_state.current_user = None

# Login page
st.sidebar.title("Login")

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

login_button = st.sidebar.button("Login")

if login_button:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Players WHERE player_id = %s AND password = %s", (username, password))
    result = cursor.fetchone()
    cursor.close()
    if result:
        session_state.logged_in = True
        session_state.current_user = username
        st.sidebar.success("Login successful!")
    else:
        st.sidebar.error("Invalid username or password")

# Sign-up page
st.sidebar.title("Sign-up")

new_username = st.sidebar.text_input("New Username")
new_password = st.sidebar.text_input("New Password", type="password")

signup_button = st.sidebar.button("Sign-up")

if signup_button:
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Players (player_id, password) VALUES (%s, %s)", (new_username, new_password))
        conn.commit()
        st.sidebar.success("Sign-up successful!")
    except mysql.connector.Error as err:
        st.sidebar.error(f"Error: {err}")

# Sign out button
if session_state.logged_in:
    if st.sidebar.button("Sign out"):
        session_state.logged_in = False
        session_state.current_user = None

# If logged in
if session_state.logged_in:
    # Function to execute SQL queries
    def execute_query(query, params=None):
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    player_ids_query = "SELECT DISTINCT player_id FROM Players"
    player_ids_result = execute_query(player_ids_query)
    player_ids = [player_id[0] for player_id in player_ids_result]

    selected_player_id = st.selectbox('Select Player ID', player_ids)

    player_kills_query = """
    SELECT s.player_id, ss.kills, ds.kills, ts.kills, sqs.kills, ltm.kills
    FROM Players s
    LEFT JOIN SoloStats ss on s.player_id = ss.player_id
    LEFT JOIN DuosStats ds on s.player_id = ds.player_id
    LEFT JOIN TriosStats ts on s.player_id = ts.player_id
    LEFT JOIN SquadsStats sqs on s.player_id = sqs.player_id
    LEFT JOIN SoloStats ltm on s.player_id = ltm.player_id
    where s.player_id = %s
    """

    player_stats_query = """
    SELECT s.player_id, 
           ss.score AS solo_score, 
           ds.score AS duos_score, 
           ts.score AS trios_score, 
           sqs.score AS squads_score, 
           ltms.score AS ltm_score
    FROM Players s
    LEFT JOIN SoloStats ss ON s.player_id = ss.player_id
    LEFT JOIN DuosStats ds ON s.player_id = ds.player_id
    LEFT JOIN TriosStats ts ON s.player_id = ts.player_id
    LEFT JOIN SquadsStats sqs ON s.player_id = sqs.player_id
    LEFT JOIN LTMStats ltms ON s.player_id = ltms.player_id
    WHERE s.player_id = %s
    """

    player_stats_params = (selected_player_id,)
    player_stats_result = execute_query(player_stats_query, player_stats_params)

    player_kills_params = (selected_player_id,)
    player_kills_result = execute_query(player_kills_query, player_kills_params)

    player_stats_df = pd.DataFrame(player_stats_result, columns=["Player ID", "Solo", "Duo", "Trio", "Squad", "LTM"])
    st.header('Player Scores Across All Game Modes')
    stats_df = player_stats_df.melt(id_vars=["Player ID"], var_name="Game Mode", value_name="Score")
    fig = px.bar(stats_df, x="Game Mode", y="Score", color="Game Mode", title=f"Scores for Player ID: {selected_player_id}")
    st.plotly_chart(fig, use_container_width=True)

    player_kills_df = pd.DataFrame(player_kills_result, columns=["Player ID", "Solo", "Duo", "Trio", "Squad", "LTM"])
    st.header('Player Kills Across All Game Modes')
    kills_df = player_kills_df.melt(id_vars=["Player ID"], var_name="Game Mode", value_name="Kills")
    fig = px.bar(kills_df, x="Game Mode", y="Kills", color="Game Mode", title=f"Kill count for Player ID: {selected_player_id}",text_auto=True)
    st.plotly_chart(fig, use_container_width=True)
    
    st.header('Player Win/Loss Percentages')
    solo = st.checkbox("View Solo Stats")
    duo = st.checkbox("View Duo Stats")
    trio = st.checkbox("View Trio Stats")
    squad = st.checkbox("View Squad Stats")
    ltm = st.checkbox("View LTM Stats")
    ph_solo = st.empty()
    ph_duo = st.empty()
    ph_trio = st.empty()
    ph_squad = st.empty()
    ph_ltm = st.empty()

    if solo:
        ph_solo.empty()
        player_wl_query = "SELECT top1, (matches_count-top1) as loss FROM SoloStats where player_id = %s"
        player_wl_result = execute_query(player_wl_query, (selected_player_id,))
        df = pd.DataFrame({"WL":['Wins', 'Losses'], "Count": [player_wl_result[0][0], player_wl_result[0][1]]})
        fig = px.pie(df, values='Count', names='WL', title="Solo W/L ratio")
        st.plotly_chart(fig, use_container_width=True)
        

    if duo:
        ph_duo.empty()
        player_wl_query = "SELECT top1, (matches_count-top1) as loss FROM DuosStats where player_id = %s"
        player_wl_result = execute_query(player_wl_query, (selected_player_id,))
        df = pd.DataFrame({"WL":['Wins', 'Losses'], "Count": [player_wl_result[0][0], player_wl_result[0][1]]})
        fig = px.pie(df, values='Count', names='WL', title="Duos W/L ratio")
        st.plotly_chart(fig, use_container_width=True)
    
    
    if trio:
        ph_trio.empty()
        player_wl_query = "SELECT top1, (matches_count-top1) as loss FROM TriosStats where player_id = %s"
        player_wl_result = execute_query(player_wl_query, (selected_player_id,))
        df = pd.DataFrame({"WL":['Wins', 'Losses'], "Count": [player_wl_result[0][0], player_wl_result[0][1]]})
        fig = px.pie(df, values='Count', names='WL', title="Trios W/L ratio")
        st.plotly_chart(fig, use_container_width=True)

            
    if squad:
        ph_squad.empty()
        player_wl_query = "SELECT top1, (matches_count-top1) as loss FROM SquadsStats where player_id = %s"
        player_wl_result = execute_query(player_wl_query, (selected_player_id,))
        df = pd.DataFrame({"WL":['Wins', 'Losses'], "Count": [player_wl_result[0][0], player_wl_result[0][1]]})
        fig = px.pie(df, values='Count', names='WL', title="Squads W/L ratio")
        st.plotly_chart(fig, use_container_width=True)

    
    if ltm:
        ph_ltm.empty()
        player_wl_query = "SELECT top1, (matches_count-top1) as loss FROM LTMStats where player_id = %s"
        player_wl_result = execute_query(player_wl_query, (selected_player_id,))
        df = pd.DataFrame({"WL":['Wins', 'Losses'], "Count": [player_wl_result[0][0], player_wl_result[0][1]]})
        fig = px.pie(df, values='Count', names='WL', title="LTM W/L ratio")
        st.plotly_chart(fig, use_container_width=True)



# Close the MySQL connection
conn.close()
