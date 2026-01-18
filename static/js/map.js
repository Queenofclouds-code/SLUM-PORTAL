const map = L.map("map").setView([18.52, 73.85], 12);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap"
}).addTo(map);

fetch("/slums")
  .then(res => res.json())
  .then(data => {
    L.geoJSON(data, {
      style: {
        color: "#ff0000",
        weight: 2,
        fillOpacity: 0.3
      },
      onEachFeature: (feature, layer) => {
        const status = feature.properties.status || "Pending";

const statusColor =
  status === "Verified" ? "green" :
  status === "Rejected" ? "red" :
  "orange";

layer.bindPopup(`
  <b>${feature.properties.name}</b><br>
  Ward: ${feature.properties.ward_no}<br>
  Zone: ${feature.properties.zone}<br>

  <b>Status:</b>
  <span style="color:${statusColor}; font-weight:600;">
    ${status}
  </span>
  <br><br>

  ${feature.properties.photo ? `
    <a href="/photos/${feature.properties.photo}" target="_blank">
      📷 View Photo
    </a><br>
  ` : ""}

  ${feature.properties.video ? `
    <video width="220" controls style="margin-top:6px;border-radius:6px;">
      <source src="/videos/${feature.properties.video}" type="video/mp4">
      Your browser does not support the video tag.
    </video>
  ` : ""}
`);


      }
    }).addTo(map);
  })
  .catch(err => console.error("GeoJSON load error:", err));
