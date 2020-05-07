document.onkeyup = function(e) {
                    if (e.which == 37) {
                        console.log("left arrow key was pressed");
                        window.location.href = #PHOTO_PREVIOUS_LINK;
                    } else if (e.which == 39) {
                        console.log("right arrow key was pressed");
                        window.location.href = #PHOTO_NEXT_LINK;
                    }
                };