import streamlit as st
import datetime

# 1. Configuration
st.set_page_config(page_title="AV Intake Tool", page_icon="🎙️")

# 2. Hardware Mapping
venue_hardware = {
    "Great Hall": "85\" Rolling TV",
        "Parlor": "House Projector",
            "Sun Room": "Credenza TV",
                "Activity Hall": "House Projector",
                    "Vista": "85\" Rolling TV"
                    }

                    # 3. Sidebar Inputs
                    st.sidebar.header("Event Details")
                    event_date = st.sidebar.date_input("Event Date", datetime.date.today() + datetime.timedelta(days=14))
                    start_time = st.sidebar.time_input("Event Start Time", datetime.time(18, 0))
                    venue = st.sidebar.selectbox("Venue", list(venue_hardware.keys()))

                    # 4. Main Body UI
                    st.title("PEF Technical Generator")
                    st.write("Fill out the details below to generate the AV Narrative.")

                    col1, col2 = st.columns(2)
                    with col1:
                        mic_type = st.selectbox("Microphone", ["Handheld", "Podium", "Headset"])
                            tech_req = st.checkbox("Technician On Site?")

                            with col2:
                                laptop_src = st.radio("Laptop Source", ["Theirs", "Ours"])

                                # 5. Logic Calculations
                                # Calculate Show Ready (1 hr prior)
                                dt_start = datetime.datetime.combine(event_date, start_time)
                                dt_ready = dt_start - datetime.timedelta(hours=1)
                                show_ready_str = dt_ready.strftime("%I:%M %p")

                                # Calculate Media Deadline (7 days prior)
                                dt_deadline = event_date - datetime.timedelta(days=7)
                                deadline_str = dt_deadline.strftime("%m/%d/%Y")

                                # 6. Build Narrative
                                lines = []
                                lines.append(f"• SHOW READY: {show_ready_str} (1 hour prior to start).")

                                # Force Tech for Headsets
                                final_tech = tech_req
                                if mic_type == "Headset":
                                    final_tech = True
                                        lines.append("• AUDIO: Headset Microphone (Technician On Site Required).")
                                        else:
                                            lines.append(f"• AUDIO: {mic_type} configuration.")

                                            lines.append(f"• VISUAL: {venue} - {venue_hardware.get(venue)}.")

                                            if final_tech:
                                                lines.append("• SPATIAL: Dedicated 4ft technical footprint required for Technician.")

                                                if laptop_src == "Ours":
                                                    lines.append(f"• MEDIA: Internal Playback (Files due by {deadline_str}).")
                                                    else:
                                                        lines.append("• INPUT: Client Laptop (Technician must verify signal path).")

                                                        # 7. Display Results
                                                        st.subheader("PEF Narrative")
                                                        st.code("\n".join(lines), language="text")

                                                        st.subheader("Client Instructions")
                                                        st.info(f"1. Show Ready: {show_ready_str}\n2. Media Due: {deadline_str}")
                                                    