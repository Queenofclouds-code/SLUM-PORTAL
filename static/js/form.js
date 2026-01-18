// ================= GEOLOCATION =================
navigator.geolocation.getCurrentPosition(
    pos => {
        document.getElementById("latitude").value =
            pos.coords.latitude.toFixed(6);
        document.getElementById("longitude").value =
            pos.coords.longitude.toFixed(6);
    },
    err => {
        alert("Please allow location access");
        console.error(err);
    },
    { enableHighAccuracy: true }
);


// ================= WIZARD LOGIC =================
const steps = document.querySelectorAll(".step");
let current = 0;

steps[current].classList.add("active");

document.querySelectorAll(".next").forEach(btn => {
    btn.addEventListener("click", () => {
        if (current < steps.length - 1) {
            steps[current].classList.remove("active");
            current++;
            steps[current].classList.add("active");
        }
    });
});

document.querySelectorAll(".prev").forEach(btn => {
    btn.addEventListener("click", () => {
        if (current > 0) {
            steps[current].classList.remove("active");
            current--;
            steps[current].classList.add("active");
        }
    });
});


// ================= FILE PREVIEW =================
const photoInput = document.getElementById("photoInput");
const videoInput = document.getElementById("videoInput");

photoInput.addEventListener("change", () => {
    document.getElementById("photoName").textContent =
        photoInput.files[0]?.name || "No photo selected";
});

videoInput.addEventListener("change", () => {
    const file = videoInput.files[0];

    if (!file) return;

    if (file.size > 40 * 1024 * 1024) {
        alert("Video must be under 40 MB");
        videoInput.value = "";
        return;
    }

    document.getElementById("videoName").textContent = file.name;
});


// ================= FORM SUBMIT =================
document.getElementById("slumForm").addEventListener("submit", async e => {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);

    try {
        const res = await fetch("/slum", {
            method: "POST",
            body: formData
        });

        if (!res.ok) {
            const text = await res.text();
            console.error(text);
            alert("Server error. Check console.");
            return;
        }

        const data = await res.json();
        alert(data.message || "Saved successfully");

        // ✅ Reset ONLY after success
        form.reset();

        // Reset wizard to step 1
        steps[current].classList.remove("active");
        current = 0;
        steps[current].classList.add("active");

        document.getElementById("photoName").textContent = "";
        document.getElementById("videoName").textContent = "";

    } catch (err) {
        console.error(err);
        alert("Network error. Please try again.");
    }
});
