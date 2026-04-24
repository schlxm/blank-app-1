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
tab1, tab2 = st.tabs(["PEF Data", "Discovery Guidelines"])

with tab1:
    st.title("PEF Technical Generator")
    
    col1, col2 = st.columns(2)
    with col1:
        mic_type = st.selectbox("Microphone Type", ["Handheld", "Podium", "Headset"])
        tech_req = st.checkbox("Technician On Site?")
        music_choice = st.selectbox("Background Music", 
            ["None", "Cocktail Jazz (Internal)", "Lofi Beats (Internal)", "Acoustic Instrumental (Internal)", "Client Provided (Spotify Link Only)"])
    
    with col2:
        laptop_src = st.radio("Laptop Source", ["Theirs", "Ours"])
        laptop_loc_choice = st.selectbox("Preferred Laptop Location", ["Podium", "Tech Table", "Other"])
        
        # Logic for "Other" fillable field
        if laptop_loc_choice == "Other":
            laptop_loc = st.text_input("Enter Location Description", placeholder="e.g. Front Row Center")
            if not laptop_loc:
                laptop_loc = "Location TBD"
        else:
            laptop_loc = laptop_loc_choice
            
        clicker_req = st.checkbox("Wireless Slide Advancer Needed?")

    # --- LOGIC ENGINE ---
    dt_start = datetime.datetime.combine(event_date, start_time)
    dt_ready = dt_start - datetime.timedelta(hours=1)
    show_ready_str = dt_ready.strftime("%I:%M %p")
    deadline_date = event_date - datetime.timedelta(days=7)
    deadline_str = deadline_date.strftime("%m/%d/%Y")

    final_tech_on_site = tech_req
    if mic_type == "Headset" or laptop_loc_choice == "Other": 
        final_tech_on_site = True

    lines = []
    lines.append(f"• SHOW READY: {show_ready_str} (1 hour prior to start).")

    # Audio Logic
    if mic_type == "Headset":
        lines.append("• AUDIO: Headset Microphone (Technician On Site Required).")
    else:
        lines.append(f"• AUDIO: {mic_type.capitalize()} configuration.")

    # Music Logic
    if music_choice == "None":
        lines.append("• MUSIC: No background music requested.")
    elif "Internal" in music_choice:
        lines.append(f"• MUSIC: Internal Playlist - {music_choice.split(' (')[0]}.")
    else:
        lines.append(f"• MUSIC: Client Spotify Link (Link due by {deadline_str}).")

    # Visual Logic
    current_screen = venue_hardware.get(venue)
    lines.append(f"• VISUAL: {venue} - {current_screen}.")
    if clicker_req:
        lines.append("• ACCESSORY: Wireless Slide Advancer provided.")
    
    # Spatial Logic
    if final_tech_on_site:
        lines.append("• SPATIAL: Tech Table required for Tech station.")

    # Input & Power Logic
    power_note = "Power and HDMI provided"
    if laptop_src == "Ours":
        lines.append(f"• MEDIA: Internal Playback (Files due by {deadline_str}). {power_note} at laptop location.")
    else:
        adapter_note = " (Include USB-C adapter at Podium)" if laptop_loc == "Podium" else ""
        lines.append(f"• INPUT: Client Laptop ({laptop_loc}). Tech must verify signal path. {power_note}{adapter_note}.")

    # Best Effort Compliance
    lines.append(f"• COMPLIANCE: Items provided after the {deadline_str} deadline (Media/Spotify/Testing) will be handled on a 'best effort' basis to protect event integrity.")

    # --- OUTPUT ---
    st.subheader("PEF Output")
    st.code("\n".join(lines), language="text")
    st.caption("Copy and paste the block above directly into the PEF.")

with tab2:
    st.header("Discovery Guidelines")
    
    st.subheader("1. Music")
    st.write('**Ask:** "Would you like background music? We have curated playlists, or you can share a Spotify link with us."')
    st.info("Technical Note: At this time, we only support Spotify for custom playlists. Due 7 days prior.")

    st.subheader("2. Movement")
    st.write('**Ask:** "Would your presenter like to move around while speaking? We can provide a headset and a wireless slide clicker so you aren\'t tethered to one location."')
    st.info("Note: Choosing a headset mandates a Tech and a Tech Table.")

    st.subheader("3. Device Location & Hardware")
    st.write('**Ask:** "Where would you prefer the laptop (or other presentation device) to live?"')
    st.markdown("""
    * **If Podium:** "We will provide power and HDMI connection for your convenience. Does your device have a standard HDMI port, or should we have a specific adapter ready for you?"
    * **If No Preference:** "I recommend our tech table. It’s the most elegant look for the room and ensures our tech can manage everything seamlessly behind the scenes."
    """)

    st.subheader("4. The Quality Guarantee (Missed Deadlines)")
    st.write('**Script:** "To ensure your event runs flawlessly, we ask for all media and testing to be completed by the 7-day deadline. For anything provided after that window, our team will provide a \'best effort\' integration to maintain the highest quality standards for your program."')
    
    st.markdown("---")
    st.info("The tech table provides a central station for the tech to perform active event management—including audio leveling, video switching, and transition timing—without intruding on the presentation space.")
    
