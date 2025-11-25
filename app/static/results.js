const albums = document.querySelectorAll(".album");
const artists = document.querySelectorAll("artist");

albums.forEach((album) => {
    const albumTitles = album.querySelectorAll(".album-title");
    albumTitles.forEach((albumTitle) => {
        const _tracks = album.querySelectorAll(".tracks");
        const covers = albumTitle.querySelectorAll("img");
        albumTitle.addEventListener("mouseup", (event) => {
            _tracks.forEach((_t) => {
                const tracks = _t.querySelectorAll(".track");
                tracks.forEach((track) => {
                    if (track.style.display  == "block") {
                        track.style.display = "none"
                        albumTitle.style.borderBottomLeftRadius = "0.5rem";
                        albumTitle.style.borderBottomRightRadius = "0.5rem";
                        covers.forEach((cover) => {
                            cover.style.borderBottomLeftRadius = "0.5rem";
                        });
                    } else {
                        track.style.display = "block"
                        albumTitle.style.borderBottomLeftRadius = "0rem";
                        albumTitle.style.borderBottomRightRadius = "0rem";
                        covers.forEach((cover) => {
                            cover.style.borderBottomLeftRadius = "0rem";
                        });
                    }
                });
            });
        });
    });
});
