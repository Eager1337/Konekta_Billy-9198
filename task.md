 # Konekta marketing website
 
 ## Complete
 - User approved public-facing site with existing approved brand, no templates.
 - Managed app initialized; web only, no new backend routes or tables.
 - Responsive landing page: hero, interactive category explorer, Protection, business, local details, FAQ, download and footer.
 - Approved logo flattened to blue; approved AI imagery; original app screenshot; fonts self-hosted.
 - Google Play and contact/legal destinations extracted from current site.
 - Light/dark mode stored locally; mobile menu; keyboard category navigation; FAQ disclosure.
 - Build and lint both pass.
 - Browser tests pass: tabs, arrow keyboard tabs, FAQ, theme persistence, mobile nav, images, no horizontal overflow at 390/768/1024/1440; no page errors.
 - Desktop, full-page, dark and mobile screenshots reviewed.
 
 ## Blocker / not included
 - Video generation attempted with approved single-scene prompt; tool returned: Video generation requires a paid Runable plan. No fake video player added.
 - Website has not replaced the user's existing live site; publishing/custom domains are platform UI actions.
 - Full downloadable brand-kit package not completed; scope moved to website on user request.
 
 ## Running
 - tmux session konekta-web; bun run dev; managed web port 4200.