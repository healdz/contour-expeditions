# Contour Expeditions

Static website for [contour-expeditions.com](https://contour-expeditions.com). It is plain HTML, CSS, and JavaScript, with no build step, and is hosted on GitHub Pages.

## Preview locally

```sh
python3 -m http.server 8000
```

Then open http://localhost:8000.

## Site map

| Page | File |
| --- | --- |
| Home | `index.html` |
| Guided Trips (listing) | `guided-trips.html` |
| Unguided Trips (listing) | `unguided-trips.html` |
| Customize Your Adventure | `customize.html` |
| About | `about.html` |
| Contact | `contact.html` |
| Trip pages | `trips/*.html` (one per trip) |

The header and footer are copied into every page. When you change the navigation or footer, for example to add a trip, update all the `.html` files. A find-and-replace across the project works well.

## Replacing placeholder content

Search the project for `TODO`, `todo`, and `data-todo` to find everything that still needs real content:

- **Prices and dates.** These are in the "At a Glance" price box and the "Dates & Prices" table on each trip page. Delete the `<span class="todo">…</span>` badges once the real values are in.
- **Booking links.** Each "Reserve" or "Waitlist" button has `href="#" data-todo="booking-link"`. Paste the booking URL (e.g. WeTravel) into the `href`. Until you do, the button sends visitors to the contact form with that trip pre-selected.
- **Forms.** The Contact and Customize forms post to Formspree:
  1. Create a free account at https://formspree.io and create a form.
  2. Replace `YOUR_FORM_ID` in the `action` attribute in `contact.html` and `customize.html`.
  3. Until you do, submitting a form shows a "not connected yet" notice.
- **Photos.** Placeholders are in `assets/img/placeholders/`. Add real photos (e.g. `assets/img/photos/peru-huayhuash.jpg`, roughly 2000px wide, compressed) and update the matching `src` attributes. Each trip's photo appears in its hero, its trip cards, and the footer strip.
- **Route maps.** Each trip page has a `data-route` attribute holding `[lat, lng, "Label"]` waypoints. The current waypoints are approximate, so replace them with real ones.
- **Social links, phone, team bios, and testimonial.** These are marked `data-todo` or `Placeholder`.

## Design

- **Colours and fonts** are CSS variables at the top of `assets/css/styles.css`. The fonts are Oswald and Inter from Google Fonts.
- **Contour background** is `assets/img/contours.svg`, a seamlessly tiling pattern. To generate a different one, run:
  ```sh
  python3 tools/generate_contours.py assets/img/contours.svg --seed 12
  ```
- **Route maps** use [Leaflet](https://leafletjs.com) and [OpenTopoMap](https://opentopomap.org) tiles, loaded from a CDN.

## Deploying to GitHub Pages

1. Push to `main`.
2. In the repo, go to **Settings → Pages**. Set Source to **Deploy from a branch** and choose `main` / `(root)`.
3. Set the custom domain to `contour-expeditions.com`. The `CNAME` file is already in the repo.
4. At your domain registrar, add these DNS records:
   - `A` records for `@`: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - A `CNAME` record for `www` pointing to `healdz.github.io`
5. Once the certificate is issued, which can take up to an hour, tick **Enforce HTTPS**.

GitHub Pages on a free account needs a public repository. A private repo requires GitHub Pro or higher.
