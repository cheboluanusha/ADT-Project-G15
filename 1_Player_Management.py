import streamlit as st
import mysql.connector
import os

# Connect to MySQL
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="root",
    database="adt_project_naman"
)
st.title("Manage Players")

# Initialize user session
session_state = st.session_state
if 'logged_in' not in session_state:
    session_state.logged_in = False
    session_state.current_user = None


if session_state.logged_in:

    with st.form("Create Player"):
        st.subheader("Create a New Player Record")
        #player_ids_query = "SELECT player_id FROM Players"
        new_stats_id = st.text_input("Stats_Id")
        new_player_id = st.text_input("Player ID")
        new_password = st.text_input("Password", type="password")
        default_score = st.number_input("Score", min_value=0)
        default_top1 = st.number_input("Top 1 Finishes", min_value=0)
        default_kdr = st.number_input("Kill/Death Ratio", min_value=0.0)
        default_matches = st.number_input("Matches Played", min_value=0)
        default_kills = st.number_input("Kills", min_value=0)
        default_minutes = st.number_input("Minutes Played", min_value=0)

        # Checkboxes for selecting game modes to insert records
        create_solo = st.checkbox('Create Solo Stats')
        create_duos = st.checkbox('Create Duos Stats')
        create_trios = st.checkbox('Create Trios Stats')
        create_squads = st.checkbox('Create Squads Stats')
        create_ltm = st.checkbox('Create LTM Stats')

        submitted = st.form_submit_button("Create Player")
        if submitted:
            cursor = conn.cursor()
            try:
                # Check if player already exists
                player_exists_query = "SELECT COUNT(*) FROM Players WHERE player_id = %s"
                cursor.execute(player_exists_query, (new_player_id,))
                player_exists = cursor.fetchone()[0]
                
                if not player_exists:
                    # Insert into Players table if player does not exist
                    players_query = "INSERT INTO Players (player_id, password) VALUES (%s, %s)"
                    cursor.execute(players_query, (new_player_id, new_password))
                    conn.commit()
                
                # Data tuple for stats tables
                stats_tuple = (new_stats_id, new_player_id, default_score, default_top1, default_kdr, default_matches, default_kills, default_minutes)
                
                # Insert into game mode stats tables based on checkbox selections
                if create_solo:
                    solo_query = "INSERT INTO SoloStats (stats_id, player_id, score, top1, kill_death_ratio, matches_count, kills, minutes_played) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(solo_query, stats_tuple)
                if create_duos:
                    duos_query = "INSERT INTO DuosStats (stats_id,player_id, score, top1, kill_death_ratio, matches_count, kills, minutes_played) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(duos_query, stats_tuple)
                if create_trios:
                    trios_query = "INSERT INTO TriosStats (stats_id,player_id, score, top1, kill_death_ratio, matches_count, kills, minutes_played) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(trios_query, stats_tuple)
                if create_squads:
                    squads_query = "INSERT INTO SquadsStats (stats_id,player_id, score, top1, kill_death_ratio, matches_count, kills, minutes_played) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(squads_query, stats_tuple)
                if create_ltm:
                    ltm_query = "INSERT INTO LTMStats (stats_id,player_id, score, top1, kill_death_ratio, matches_count, kills, minutes_played) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(ltm_query, stats_tuple)

                conn.commit()
                st.success("Player created successfully in selected game modes!")
            except mysql.connector.Error as e:
                conn.rollback()
                st.error(f"Failed to create player: {e}")


    # Update a player record
    with st.form("Update Player"):
        st.subheader("Update Player Record")
        
        player_ids_query = "SELECT player_id FROM Players"
        cursor = conn.cursor()
        cursor.execute(player_ids_query)
        player_ids_result = cursor.fetchall()
        player_ids = [player_id[0] for player_id in player_ids_result]
        cursor.close()
        
        player_id_to_update = st.selectbox("Select Player ID to Update", player_ids)  # This function fetches player IDs from the database
        
        # Input field for password verification
        password = st.text_input("Enter Password", type="password")
        
        # Dropdown to select game mode to update
        game_mode_options = ['Solo Stats', 'Duos Stats', 'Trios Stats', 'Squads Stats', 'LTM Stats']
        selected_game_mode = st.selectbox("Select Game Mode to Update", game_mode_options)
        
        update_submitted = st.form_submit_button("Update Player")
        if update_submitted:
            cursor = conn.cursor()
            try:
                # Verify password before proceeding with update
                verify_password_query = "SELECT COUNT(*) FROM Players WHERE player_id = %s AND password = %s"
                cursor.execute(verify_password_query, (player_id_to_update, password))
                password_verified = cursor.fetchone()[0]
                
                if password_verified:
                    # Update stats table based on selected game mode
                    if selected_game_mode == 'Solo Stats':
                        update_stats_query = "UPDATE SoloStats SET score = %s, top1 = %s, kill_death_ratio = %s, matches_count = %s, kills = %s, minutes_played = %s WHERE player_id = %s"
                    elif selected_game_mode == 'Duos Stats':
                        update_stats_query = "UPDATE DuosStats SET score = %s, top1 = %s, kill_death_ratio = %s, matches_count = %s, kills = %s, minutes_played = %s WHERE player_id = %s"
                    elif selected_game_mode == 'Trios Stats':
                        update_stats_query = "UPDATE TriosStats SET score = %s, top1 = %s, kill_death_ratio = %s, matches_count = %s, kills = %s, minutes_played = %s WHERE player_id = %s"
                    elif selected_game_mode == 'Squads Stats':
                        update_stats_query = "UPDATE SquadsStats SET score = %s, top1 = %s, kill_death_ratio = %s, matches_count = %s, kills = %s, minutes_played = %s WHERE player_id = %s"
                    elif selected_game_mode == 'LTM Stats':
                        update_stats_query = "UPDATE LTMStats SET score = %s, top1 = %s, kill_death_ratio = %s, matches_count = %s, kills = %s, minutes_played = %s WHERE player_id = %s"
                    
                    # Fetch existing stats values for the selected player
                    get_stats_query = f"SELECT * FROM {selected_game_mode.replace(' ', '')} WHERE player_id = %s"
                    cursor.execute(get_stats_query, (player_id_to_update,))
                    stats_data = cursor.fetchone()
                    
                    # If stats exist, update them
                    if stats_data:
                        updated_score = st.number_input("Update Score", min_value=0.0, value=float(stats_data[2]))
                        updated_top1 = st.number_input("Update Top 1 Finishes", min_value=0, value=int(stats_data[3]))
                        updated_kdr = st.number_input("Update Kill/Death Ratio", min_value=0.0, value=float(stats_data[4]))
                        updated_matches = st.number_input("Update Matches Played", min_value=0, value=int(stats_data[5]))
                        updated_kills = st.number_input("Update Kills", min_value=0, value=int(stats_data[6]))
                        updated_minutes = st.number_input("Update Minutes Played", min_value=0, value=int(stats_data[7]))
                        
                        cursor.execute(update_stats_query, (updated_score, updated_top1, updated_kdr, updated_matches, updated_kills, updated_minutes, player_id_to_update))
                        conn.commit()
                        st.success("Player stats updated successfully!")
                    else:
                        st.warning("No existing stats found for this player in the selected game mode.")
                
                else:
                    st.error("Incorrect password. Update failed.")
                    
            except mysql.connector.Error as e:
                conn.rollback()
                st.error(f"Failed to update player: {e}")
            finally:
                cursor.close()


    # Delete a player record
    with st.form("Delete Player"):
        st.subheader("Delete Player Record")

        # Query to fetch player IDs from the database
        player_ids_query = "SELECT player_id FROM Players"
        cursor = conn.cursor()
        cursor.execute(player_ids_query)
        player_ids_result = cursor.fetchall()
        player_ids = [player_id[0] for player_id in player_ids_result]
        cursor.close()

        delete_player_id = st.selectbox("Select Player ID to Delete", player_ids)  # Dynamically populate player IDs from the database
        
        # Input field for password verification
        password = st.text_input("Enter Password", type="password")

        delete_submitted = st.form_submit_button("Delete Player")

        if delete_submitted:
            cursor = conn.cursor()
            try:
                # Verify password before proceeding with deletion
                verify_password_query = "SELECT COUNT(*) FROM Players WHERE player_id = %s AND password = %s"
                cursor.execute(verify_password_query, (delete_player_id, password))
                password_verified = cursor.fetchone()[0]

                if password_verified:
                    # Delete related records first
                    delete_stats_query = "DELETE FROM SoloStats WHERE player_id = %s"
                    cursor.execute(delete_stats_query, (delete_player_id,))
                    delete_stats_query = "DELETE FROM DuosStats WHERE player_id = %s"
                    cursor.execute(delete_stats_query, (delete_player_id,))
                    delete_stats_query = "DELETE FROM TriosStats WHERE player_id = %s"
                    cursor.execute(delete_stats_query, (delete_player_id,))
                    delete_stats_query = "DELETE FROM SquadsStats WHERE player_id = %s"
                    cursor.execute(delete_stats_query, (delete_player_id,))
                    delete_stats_query = "DELETE FROM LTMStats WHERE player_id = %s"
                    cursor.execute(delete_stats_query, (delete_player_id,))

                    # Then delete the player record
                    delete_query = "DELETE FROM Players WHERE player_id = %s"
                    cursor.execute(delete_query, (delete_player_id,))

                    conn.commit()
                    st.success("Player deleted successfully!")
                else:
                    st.error("Incorrect password. Deletion failed.")

            except mysql.connector.Error as e:
                conn.rollback()
                st.error(f"Failed to delete player: {e}")
            finally:
                cursor.close()

    # Close the MySQL connection
    conn.close()
