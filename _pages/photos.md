---
layout: single
title: "Photos"
permalink: /photos/
author_profile: false
---

Selected photos.

<style>
  .photo-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1rem;
  }

  .photo-card {
    position: relative;
    margin: 0;
    overflow: hidden;
    border-radius: 8px;
  }

  .photo-card img {
    display: block;
    width: 100%;
    height: 320px;
    object-fit: cover;
  }

  .photo-card figcaption {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    margin: 0;
    padding: 0.75rem 0.9rem;
    color: #fff;
    font-size: 0.92rem;
    line-height: 1.35;
    background: linear-gradient(180deg, rgba(0, 0, 0, 0.05) 0%, rgba(0, 0, 0, 0.82) 100%);
    opacity: 0;
    transform: translateY(12px);
    transition: opacity 180ms ease, transform 180ms ease;
    pointer-events: none;
  }

  .photo-card:hover figcaption,
  .photo-card:focus-within figcaption {
    opacity: 1;
    transform: translateY(0);
  }
</style>

<p><a href="#talks-events">Talks &amp; Events</a> | <a href="#milestones">Milestones</a></p>

<h2 id="talks-events">Talks &amp; Events</h2>
<div class="photo-grid">
  <figure class="photo-card">
    <img src="/images/personal_photos/World_Cities_Summit_2022_Panel_Discussion.jpg" alt="World Cities Summit 2022 panel discussion" title="World Cities Summit 2022 panel discussion" />
    <figcaption>World Cities Summit 2022 panel discussion</figcaption>
  </figure>
  <figure class="photo-card">
    <img src="/images/personal_photos/miscellaneous/ICRS_2022_talk_on_rescue_routing.JPG" alt="ICRS talk on rescue routing" title="ICRS talk on rescue routing" />
    <figcaption>ICRS talk on rescue routing</figcaption>
  </figure>
  <figure class="photo-card">
    <img src="/images/personal_photos/miscellaneous/ICRS_2022_talk_on_rescue_routing_2.JPG" alt="ICRS talk on rescue routing (second photo)" title="ICRS talk on rescue routing (second photo)" />
    <figcaption>ICRS talk on rescue routing (second photo)</figcaption>
  </figure>
  <figure class="photo-card">
    <img src="/images/personal_photos/miscellaneous/Time_series_anomaly_detection_is_hard_so_hide_it_in_smiles.jpeg" alt="Talk moment: time-series anomaly detection" title="Talk moment: Time-series anomaly detection" />
    <figcaption>Talk moment: Time-series anomaly detection</figcaption>
  </figure>
</div>

<h2 id="milestones">Milestones</h2>
<div class="photo-grid">
  <figure class="photo-card">
    <img src="/images/personal_photos/ETH_Graduation_July_2025.jpg" alt="ETH Graduation July 2025" title="ETH Graduation, July 2025" />
    <figcaption>ETH Graduation, July 2025</figcaption>
  </figure>
  <figure class="photo-card">
    <img src="/images/personal_photos/TCS_GOld_medal_from_Prof_Dr_Leslie_Valiant.png" alt="TCS Gold Medal recognition" title="TCS Gold Medal from Prof. Leslie Valiant" />
    <figcaption>TCS Gold Medal from Prof. Leslie Valiant</figcaption>
  </figure>
  <figure class="photo-card">
    <img src="/images/personal_photos/miscellaneous/Defense_date_apero_invitation.jpeg" alt="Defense day apero invitation" title="Defense day apero invitation" />
    <figcaption>Defense day apero invitation</figcaption>
  </figure>
  <figure class="photo-card">
    <img src="/images/personal_photos/miscellaneous/Smiles_After_succeful_Defense.JPG" alt="After successful defense" title="Smiles after successful defense" />
    <figcaption>Smiles after successful defense</figcaption>
  </figure>
  <figure class="photo-card">
    <img src="/images/personal_photos/miscellaneous/With_MIE_lab_members_on_Apero_on_Graduation_day.jpeg" alt="With MIE Lab members on graduation day" title="With MIE Lab members on apero day of graduation" />
    <figcaption>With MIE Lab members on apero day of graduation</figcaption>
  </figure>
  <figure class="photo-card">
    <img src="/images/personal_photos/miscellaneous/With_my_phd_guide_and_the_external_examiners_after_defense.jpeg" alt="With PhD guide and external examiners" title="With PhD guide and external examiners after defense" />
    <figcaption>With PhD guide and external examiners after defense</figcaption>
  </figure>
  <figure class="photo-card">
    <img src="/images/personal_photos/miscellaneous/Time_to_cool_off_the_head_literataly_when_the_model_doesnt_make_any_sense.jpeg" alt="Post-defense cool-off moment" title="Post-defense cool-off moment" />
    <figcaption>Post-defense cool-off moment</figcaption>
  </figure>
</div>
