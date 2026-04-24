import streamlit as st
import datetime

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
        bgm_on = st.toggle("Include Background Music (BGM)?", value=True)
        if bgm_on:
            music_choice = st.selectbox("Playlist Selection", 
                ["Cocktail Jazz (Internal)", "Lofi Beats (Internal)", "Acoustic Instrumental (Internal)", "Client Provided (Spotify Link Only)"])
    
    with col_a2:
        mics_on = st.toggle("Include Microphones?", value=False)
        if mics_on:
            mic_type = st.selectbox("Microphone Type", ["Handheld", "Podium", "Headset"])

    st.divider()

    # --- VISUAL SECTION ---
    st.header("Visual Setup")
    visual_on = st.toggle("Visual Needs?", value=False)
    
    if visual_on:
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            pres_src = st.radio("Presentation Source", ["Theirs", "Ours"])
            clicker_req = st.checkbox("Wireless Slide Advancer Needed?")
        
        with col_v2:
            laptop_loc_choice = st.selectbox("Preferred Device Location", ["Podium", "Tech Table", "Other"])
            if laptop_loc_choice == "Other":
                laptop_loc = st.text_input("Enter Location Description", placeholder="e.g. Front Row Center")
                if not laptop_loc:
                    laptop_loc = "Location TBD"
            else:
                laptop_loc = laptop_loc_choice

    st.divider()

    # --- PERSONNEL SECTION ---
    st.header("Personnel & Support")
    tech_req = st.checkbox("Technician On Site?")

    # --- LOGIC ENGINE ---
    dt_start = datetime.datetime.combine(event_date, start_time)
    dt_ready = dt_start - datetime.timedelta(hours=1)
    show_ready_str = dt_ready.strftime("%I:%M %p")
    deadline_date = event_date - datetime.timedelta(days=7)
    deadline_str = deadline_date.strftime("%m/%d/%Y")

    lines = []
    lines.append(f"• SHOW READY: {show_ready_str} at {venue}.")

    # Audio Logic
    if mics_on:
        if mic_type == "Headset":
            lines.append("• AUDIO: Headset Microphone (Technician On Site Required).")
        else:
            lines.append(f"• AUDIO: {mic_type.capitalize()} configuration.")
    
    if bgm_on:
        if "Internal" in music_choice:
            lines.append(f"• MUSIC: Internal Playlist - {music_choice.split(' (')[0]}.")
        else:
            lines.append(f"• MUSIC: Client Spotify Link (Link due by {deadline_str}).")
    else:
        lines.append("• MUSIC: No background music requested.")

    # Visual Logic
    if visual_on:
        current_screen = venue_hardware.get(venue)
        lines.append(f"• VISUAL: {venue} - {current_screen}.")
        if clicker_req:
            lines.append("• ACCESSORY: Wireless Slide Advancer provided.")
        
        # Spatial/Power/Input
        power_note = "Power and HDMI provided"
        if pres_src == "Ours":
            lines.append(f"• MEDIA: Internal Playback (Files due by {deadline_str}). {power_note} at device location.")
        else:
            adapter_note = " (Include USB-C adapter at Podium)" if laptop_loc == "Podium" else ""
            lines.append(f"• INPUT: Client Device ({laptop_loc}). Tech must verify signal path. {power_note}{adapter_note}.")

    # Spatial / Tech Table Logic
    needs_tech_table = tech_req
    if mics_on and mic_type == "Headset": needs_tech_table = True
    if visual_on and laptop_loc_choice == "Other": needs_tech_table = True
    
    if needs_tech_table:
        lines.append("• SPATIAL: Tech Table required for Tech station.")

    # --- OUTPUT ---
    st.subheader("PEF Data")
    st.code("\n".join(lines), language="text")
    st.caption("Copy and paste the block above directly into the PEF.")

with tab2:
    st.header("Guidelines")
    
    st.subheader("1. Music")
    st.write('**Ask:** "Would you like background music? We have curated playlists, or you can share a Spotify link with us."')
    st.info("Note: At this time, we only support Spotify for custom playlists. Due 7 days prior.")

    st.subheader("2. Movement")
    st.write('**Ask:** "Would your presenter like to move around while speaking? We can provide a headset and a wireless slide clicker so you aren\'t tethered to one location."')
    st.info("Note: Choosing a headset mandates a Tech and a Tech Table.")

    st.subheader("3. Device Location")
    st.write('**Ask:** "Where would you prefer the laptop (or other presentation device) to live?"')
    st.markdown("""
    * **If Podium:** "We will provide power and HDMI connection for your convenience. Does your device have a standard HDMI port, or should we have a specific adapter ready for you?"
    * **If No Preference:** "I recommend our tech table. It’s the most elegant look for the room and ensures our tech can manage everything seamlessly behind the scenes."
    """)

    st.info("Note: The tech table provides a central station for the tech to perform active event management—including audio leveling, video switching, and transition timing—without intruding on the presentation space.")

    st.subheader("4. Deadlines")
    st.write('**Say:** "To ensure your event runs flawlessly, we ask for all presentational media (slides, video, and custom Spotify playlists) to be delivered 7 days before the event for testing on our devices. If media is to be played from a client device, we instead ask for the device(s) to arrive at the venue 1 hour before the event for testing."')
    st.write('**Say:** "For anything after these windows, our team will provide a best effort integration, but cannot guarantee technical stability."')
    
