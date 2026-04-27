import streamlit as st
import datetime

# --- INITIALIZE SESSION STATE ---
if 'handhelds' not in st.session_state:
    st.session_state.handhelds = 0
if 'headsets' not in st.session_state:
    st.session_state.headsets = 0
MAX_WIRELESS = 4

# 1. Configuration & Venue Mapping
st.set_page_config(page_title="AV Intake Tool", page_icon="🎙️")

venue_hardware = {
    "Great Hall": "85\" Rolling TV",
    "Parlor": "House Projector",
    "Sun Room": "Credenza TV",
    "Activity Hall": "House Projector",
    "Vista": "85\" Rolling TV"
}

# 2. Sidebar Navigation
st.sidebar.header("Event Logistics")
event_date = st.sidebar.date_input("Event Date", datetime.date.today() + datetime.timedelta(days=14))
start_time = st.sidebar.time_input("Event Start Time", datetime.time(18, 0))
venue = st.sidebar.selectbox("Venue Location", list(venue_hardware.keys()))

# 3. Main Interface Tabs
tab1, tab2 = st.tabs(["Tech Selector", "Discovery Guidelines"])

with tab1:
    # --- AUDIO SECTION ---
    st.header("Audio Setup")
    col_a1, col_a2 = st.columns(2)
    
    with col_a1:
        # BGM default set to False for a clean slate
        bgm_on = st.toggle("Include Background Music (BGM)", value=False)
        if bgm_on:
            music_choice = st.selectbox("Playlist Selection", 
        
        ["Cocktail Jazz (Internal)", "Lofi Beats (Internal)", "Acoustic Instrumental (Internal)", "Client Provided (Spotify Link Only)"])
    
    with col_a2:
        mics_on = st.toggle("Include Microphones", value=False)
        if mics_on:
            st.write("**Wireless Selection**")
            max_handheld = MAX_WIRELESS - st.session_state.headsets
            max_headset = MAX_WIRELESS - st.session_state.handhelds
    
        
            st.number_input("Handheld Mics", min_value=0, max_value=max_handheld, key='handhelds')
            st.number_input("Headset Mics", min_value=0, max_value=max_headset, key='headsets')
            podium_on = st.checkbox("Podium Mic")
        else:
            podium_on = False

    st.divider()

    # --- VISUAL SECTION ---
    st.header("Visual Setup")
    visual_on = st.toggle("Visual Needs", value=False)
    
    if visual_on:
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            pres_src = st.radio("Presentation Source", ["Theirs", "Ours"])
            clicker_req = st.checkbox("Wireless Slide Advancer Needed")
        
        with col_v2:
            laptop_loc_choice = st.selectbox("Preferred Device Location", ["Podium", "Tech Table", "Other"])
            if laptop_loc_choice == "Other":
                laptop_loc = st.text_input("Enter Location Description", placeholder="e.g. Front Row Center")
                if not laptop_loc:
                    laptop_loc = "Location TBD"
            else:
                laptop_loc = laptop_loc_choice

    st.divider()

    # --- EXTRA SUPPORT SECTION ---
    st.header("Extra Support")
    st.write("**Personnel**")
    tech_req = st.checkbox("Technician On Site")
 
    # Gatekeeper Flags
    st.write("**Equipment**")
    second_screen = st.checkbox("Second Screen")
    lapel_mics = st.checkbox("Lapel Mics")

    # --- LOGIC ENGINE ---
    dt_start = datetime.datetime.combine(event_date, start_time)
    dt_ready = dt_start - datetime.timedelta(hours=1)
    show_ready_str = dt_ready.strftime("%I:%M %p")
    deadline_date = event_date - datetime.timedelta(days=7)
    deadline_str = deadline_date.strftime("%m/%d/%Y")

    # Secure counts to 0 if toggled off
    handheld_count = st.session_state.handhelds if mics_on else 0
    headset_count = st.session_state.headsets if mics_on else 0

    # Gatekeeper evaluation
    requires_tech_approval = second_screen or lapel_mics

    # Personnel Logic calculated first
    final_tech_req = tech_req

    if mics_on and headset_count > 0:
        final_tech_req = True
            
    if visual_on and laptop_loc_choice == "Other":
        final_tech_req = True

    # Determine if Tech Table is needed based on final Tech requirement
    
    final_table_req = False
    if final_tech_req:
        final_table_req = True
        # Apply the special room exception
        if venue in ["Activity Hall", "Parlor", "Great Hall"] and not visual_on:
