const swiper = new Swiper('.swiper', {
             loop: true,
             allowTouchMove: true,
             effect: 'coverflow',
             grabCursor: true,
             centeredSlides: true,
             slidesPerView: 'auto',
             coverflowEffect: {
                 rotate: 50,
                 stretch: 0,
                 depth: 100,
                 modifier: 1,
                 slideShadows: true,
             },
         });

         function swipeLeft() {
             console.log('Пропустить');
             swiper.slideNext();
             const memeID = button.getAttribute('data-meme-id')
             sendSwipe(memeID, 'dislike');
         }



function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

        function sendSwipe(memeId, action) {
    fetch('/swipe/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
            meme_id: memeId,
            action: action,
        }),
    }).then(response => response.json()).then(data => {
        console.log('Swipe saved:', data);
    });
}

        function sendSave(memeId) {
    fetch('/save/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
            meme_id: memeId
        }),
    }).then(response => response.json()).then(data => {
        console.log('Meme saved:', data);
    });
}
            function toggleLike(button) {
    const img = button.querySelector('img');
    const memeId = button.getAttribute('data-meme-id');

    // Toggle heart icon image
    if (img.src.includes("heartEmpty.png")) {
        img.src = "{% static 'images/heartFull.png' %}";
        console.log("Liked meme", memeId);
        sendSwipe(memeId, 'like');
    } else {
        img.src = "{% static 'images/heartEmpty.png' %}";
        console.log("Unliked meme", memeId);
        sendSwipe(memeId, 'unlike');
    }
}


         function toggleSave(button) {
             const img = button.querySelector('img');
             if (img.src.includes("{% static 'images/saveEmpty.png' %}")) {
                 img.src = "{% static 'images/saveFull.png' %}";
                 console.log('Мем сохранён');
             } else {
                 img.src = "{% static 'images/saveEmpty.png' %}";
                 console.log('Сохранение отменено');
             }
         }

         function goNext() {
             swiper.slideNext();
             console.log('Следующий мем');
         }