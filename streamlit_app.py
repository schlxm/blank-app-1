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
# Venue selection now informs the visual hardware output
venue = st.sidebar.selectbox("Venue Location", list(venue_hardware.keys()))

# 3. Main Interface Tabs
tab1, tab2 = st.tabs(["PEF Generator", "Help & Discovery Script"])

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
        laptop_loc = st.selectbox("Preferred Laptop Location", 
            ["Podium", "Front Row", "Tech Table", "No Preference / Upsell Tech Table"])
        clicker_req = st.checkbox("Wireless Slide Advancer Needed?")

    # --- LOGIC ENGINE ---
    dt_start = datetime.datetime.combine(event_date, start_time)
    dt_ready = dt_start - datetime.timedelta(hours=1)
    show_ready_str = dt_ready.strftime("%I:%M %p")
    deadline_str = (event_date - datetime.timedelta(days=7)).strftime("%m/%d/%Y")

    # Force tech table/labor for headset or the "No Preference" upsell
    final_tech_on_site = tech_req
    if mic_type == "Headset" or laptop_loc == "No Preference / Upsell Tech Table":
        final_tech_on_site = True

    lines = []
    lines.append(f"• SHOW READY: {show_ready_str} (1 hour prior to start).")

    # Audio Logic
    if mic_type == "Headset":
        lines.append("• AUDIO: Headset Microphone (Technician On Site Required).")
    else:
        lines.append(f"• AUDIO: {mic_type.capitalize()} configuration.")

    # Music Logic
    if music_choice != "None":
        if "Internal" in music_choice:
            lines.append(f"• MUSIC: Internal Playlist - {music_choice.split(' (')[0]}.")
        else:
            lines.append(f"• MUSIC: Client Spotify Link (Link due by {deadline_str}).")

    # Visual Logic (Driven by Venue Selection)
    current_screen = venue_hardware.get(venue)
    lines.append(f"• VISUAL: {venue} - {current_screen}.")
    if clicker_req:
        lines.append("• ACCESSORY: Wireless Slide Advancer provided.")
    
    # Spatial Logic
    if final_tech_on_site:
        lines.append("• SPATIAL: 4ft Tech Table required for Technician.")

    # Input & Power Logic
    power_note = "Power and HDMI connectivity provided at laptop location."
    if laptop_src == "Ours":
        lines.append(f"• MEDIA: Internal Playback (Files due by {deadline_str}). {power_note}")
    else:
        lines.append(f"• INPUT: Client Laptop (Technician must verify signal path). {power_note}")

    # --- OUTPUT ---
    st.subheader("PEF Narrative Output")
    st.code("\n".join(lines), language="text")
    st.caption("Copy and paste the block above directly into the PEF.")

with tab2:
    st.header("Discovery Flow Chart & Script")
    
    st.subheader("1. The Music Question")
    st.write("**Ask:** 'Would you like background music? We have curated lists, or you can share a **Spotify link** with us.'")
    st.info("Technical Note: We only support Spotify for custom links. Due 7 days prior.")

    st.subheader("2. The Movement Question")
    st.write("**Ask:** 'Would you like to move around while speaking? We can provide a headset and a wireless slide clicker so you aren't tethered to the laptop.'")
    st.warning("Note: Choosing a headset mandates a Technician and a 4ft Tech Table.")

    st.subheader("3. The 'Pampered' Placement")
    st.write("**Ask:** 'Where would you prefer the laptop to live?'")
    st.write("**If No Preference (The Upsell):** 'I recommend our 4ft Tech Table. It’s the most elegant look for the room and ensures our technician can manage everything seamlessly behind the scenes.'")
    
    st.markdown("---")
    st.header("Technician Justification (Internal Only):")
    st.write("- **The 4ft Table:** Provides a 'home base' for the tech to manage audio levels and Spotify transitions without interrupting the event flow.")
    st.write("- **Connectivity:** We handle the adapters and power so the client feels taken care of.")
