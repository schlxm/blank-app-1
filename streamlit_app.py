import streamlit as st
import datetime

# --- INITIALIZE SESSION STATE ---
if 'handhelds' not in st.session_state:
    st.session_state.handhelds = 0
if 'headsets' not in st.session_state:
    st.session_state.headsets = 0
MAX_WIRELESS = 4

# 1. [span_0](start_span)Configuration & Venue Mapping[span_0](end_span)
st.set_page_config(page_title="AV Intake Tool", page_icon="🎙️")

venue_hardware = {
    "Great Hall": "85\" Rolling TV",
    "Parlor": "House Projector",
    "Sun Room": "Credenza TV",
    "Activity Hall": "House Projector",
    "Vista": "85\" Rolling TV"
}

# 2. [span_1](start_span)Sidebar Navigation[span_1](end_span)
st.sidebar.header("Event Logistics")
event_date = st.sidebar.date_input("Event Date", datetime.date.today() + datetime.timedelta(days=14))
start_time = st.sidebar.time_input("Event Start Time", datetime.time(18, 0))
venue = st.sidebar.selectbox("Venue Location", list(venue_hardware.keys()))

# 3. [span_2](start_span)Main Interface[span_2](end_span)
tab1, tab2 = st.tabs(["Tech Selector", "Discovery Guidelines"])

with tab1:
    # --- AUDIO SECTION ---
    st.header("Audio Setup")
    col_a1, col_a2 = st.columns(2)
    
    with col_a1:
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
            # [span_3](start_span)Updated terminology[span_3](end_span)
            clicker_req = st.checkbox("Wireless Slide Remote Needed")
        
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
 
    st.write("**Equipment**")
    second_screen = st.checkbox("Second Screen")
    lapel_mics = st.checkbox("Lapel Mics")

    # --- LOGIC ENGINE ---
    dt_start = datetime.datetime.combine(event_date, start_time)
    dt_ready = dt_start - datetime.timedelta(hours=1)
    show_ready_str = dt_ready.strftime("%I:%M %p")
    deadline_date = event_date - datetime.timedelta(days=7)
    deadline_str = deadline_date.strftime("%m/%d/%Y")

    handheld_count = st.session_state.handhelds if mics_on else 0
    headset_count = st.session_state.headsets if mics_on else 0
    requires_tech_approval = second_screen or lapel_mics
    final_tech_req = tech_req

    if mics_on and headset_count > 0:
        final_tech_req = True
            
    if visual_on and laptop_loc_choice == "Other":
        final_tech_req = True

    final_table_req = False
    if final_tech_req:
        final_table_req = True
        if venue in ["Activity Hall", "Parlor", "Great Hall"] and not visual_on:
            final_table_req = False

    lines = []
    lines.append("=== LOGISTICS & SUPPORT ===")
    lines.append(f"SHOW READY:\n{show_ready_str} ({venue})")
  
    if final_tech_req:
        lines.append("Personnel:\nTech On Site")
        if final_table_req:
            lines.append("Spatial:\nTech Table")
    else:
        lines.append("Personnel:\nNone requested/required")

    lines.append("\n=== AUDIO ===")
    if mics_on and (handheld_count > 0 or headset_count > 0 or podium_on):
        mic_details = []
        if handheld_count > 0: mic_details.append(f"{handheld_count}x Handheld")
        if headset_count > 0: mic_details.append(f"{headset_count}x Headset")
        if podium_on: mic_details.append("1x Podium")
        lines.append("Microphones:\n" + ", ".join(mic_details))
    else:
        lines.append("Microphones:\nNone")
    
    if bgm_on:
        if "Internal" in music_choice:
            lines.append(f"Music:\nInternal Playlist - {music_choice.split(' (')[0]}")
        else:
            lines.append(f"Music:\nClient Spotify Link (Due {deadline_str})")
    else:
        lines.append("Music:\nNo background music requested")

    lines.append("\n=== VISUAL ===")
    if visual_on:
        current_screen = venue_hardware.get(venue)
        lines.append(f"Display:\n{venue} - {current_screen}")
        
        power_note = "Power and HDMI provided"
        if pres_src == "Ours":
            lines.append(f"Source:\nInternal Playback (Files due {deadline_str})\n{power_note} at device location.")
        else:
            adapter_note = "\n(Include USB-C adapter at Podium)" if laptop_loc == "Podium" else ""
            lines.append(f"Source:\nClient Device ({laptop_loc})\n{power_note}.{adapter_note}")
            
        if clicker_req:
            # [span_4](start_span)Updated terminology[span_4](end_span)
            lines.append("Accessory:\nWireless Slide Remote provided.")
    else:
        lines.append("Visual:\nNone requested")

    st.subheader("PEF Data")
    if requires_tech_approval:
        st.error("### STATUS: PENDING AV APPROVAL\nEquipment or routing requested (e.g., Second Screen, Lapel Mics). **Call AV Team to resolve before finalizing PEF.**")
    else:
        st.code("\n".join(lines), language="text")
        st.caption("Copy and paste the block above directly into the PEF.")

with tab2:
    # 1. [span_5](start_span)Music[span_5](end_span)
    st.subheader("1. Music")
    st.write('**Ask:** "Would you like background music? We have curated playlists, or you can share a Spotify link with us."')
    st.info("Note: At this time, we only support Spotify for custom playlists. Due 7 days prior.")

    # 2. [span_6](start_span)Mic Selection (Updated Section)[span_6](end_span)
    st.subheader("2. Mic Selection")
    st.write('**Ask:** "What kind of mic(s) would you like?"')
    st.markdown("""
    * **Handheld:** "Many clients enjoy the flexibility of a wireless handheld on a stand."
    * **Headset:** "Some clients enjoy using a headset, as seen in TED Talks."
    * **Podium:** "We also have a gooseneck podium mic, for a refined look."
    """)
    st.info("Note: Headset mics require a tech and a tech station.")

    # 3. [span_7](start_span)Device Location[span_7](end_span)
    st.subheader("3. Device Location")
    st.write('**Ask:** "Where would you like the presentation device to be located?"')
    st.markdown("""
    * **If Podium:** "We will provide power and HDMI for your convenience. Does your device have a standard HDMI port, or should we have an adapter ready for you?"
    * **If No Preference:** "I recommend our tech table. It maintains the cleanest room aesthetic and ensures our tech can manage transitions seamlessly behind the scenes."
    """)
    st.info("Note: The tech table provides a central station for active event management—including audio leveling and transition timing—without intruding on the presentation space.")

    # 4. [span_8](start_span)Testing & Media (Updated "Support Approach")[span_8](end_span)
    st.subheader("4. Testing & Media")
    st.write('**Ask:** "Many clients like using their own device to play back media (such as a slide deck or video). If you prefer, we can provide a dedicated playback system."')
    st.markdown("""
    * **If using Client's Device,** **Say:** "To provide the best support, we ask that you and your device are on-site 1 hour early for a final check of the setup."
    * **If using House Device,** **Say:** "Great. We just need your media 7 days before the event so we can pre-load and test everything for you."
    """)
    st.info("Note: For anything after these windows, our team will provide a best effort integration, but cannot guarantee technical stability.")
