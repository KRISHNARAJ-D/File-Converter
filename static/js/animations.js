document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.getElementById("file-input");
    const dropArea = document.getElementById("drop-area");
    const fileUploadBtn = document.getElementById("file-upload-btn");
    const convertBtn = document.getElementById("convert-btn");
    const progressBar = document.getElementById("progress-bar");

    // Drag-and-Drop Effects
    dropArea.addEventListener("dragover", (e) => {
        e.preventDefault();
        dropArea.classList.add("border-blue-400");
    });

    dropArea.addEventListener("dragleave", () => {
        dropArea.classList.remove("border-blue-400");
    });

    dropArea.addEventListener("drop", (e) => {
        e.preventDefault();
        dropArea.classList.remove("border-blue-400");
        fileInput.files = e.dataTransfer.files;
        alert("Files uploaded successfully!");
    });

    // File Upload Button Trigger
    fileUploadBtn.addEventListener("click", () => fileInput.click());

    // Convert Button Click
    convertBtn.addEventListener("click", () => {
        progressBar.classList.remove("hidden");
        const progressBarInner = progressBar.querySelector("div > div");
        gsap.to(progressBarInner, {
            width: "100%",
            duration: 3,
            onComplete: () => {
                alert("Conversion Completed!");
                progressBar.classList.add("hidden");
                progressBarInner.style.width = "0%";
            },
        });
    });
});
