(function() {
    function init() {
    let startPos = null;
    let endPos = null;

    interact('.drag-drop').draggable({
        snap: {
        targets: [startPos],
        range: Infinity,
        relativePoints: [ { x: 0.5, y: 0.5 } ],
        endOnly: true
        },
        onstart: function (event) {
            var rect = interact.getElementRect(event.target);
            // record center point when starting the very first a drag
            startPos = {
                x: rect.left + rect.width  / 2,
                y: rect.top  + rect.height / 2
            }
            event.interactable.draggable({
                snap: {
                targets: [startPos]
                }
            });
        },
        // call this function on every dragmove event
        onmove: function (event) {
            var target = event.target,
                // keep the dragged position in the data-x/data-y attributes
                x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx,
                y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy;
            // translate the element
            target.style.webkitTransform =
            target.style.transform =
                'translate(' + x + 'px, ' + y + 'px)';
            // update the posiion attributes
            target.setAttribute('data-x', x);
            target.setAttribute('data-y', y);
            target.classList.add('getting--dragged');
        },
        onend: function (event) {
            event.target.classList.remove('getting--dragged')
        }
    });

    interact('.dropzone').dropzone({
        accept: '.drag-drop',
        overlap: .5,
        ondropactivate: function (event) {
            event.target.classList.add('can--drop');
        },
        ondragenter: function (event) {
            event.target.classList.add('drop-target')
            var draggableElement = event.relatedTarget,
                dropzoneElement  = event.target,
                dropRect         = interact.getElementRect(dropzoneElement),
                dropCenter       = {
                    x: dropRect.left + dropRect.width  / 2,
                    y: dropRect.top  + dropRect.height / 2
                };
            endPos = {
                    x: dropRect.left + dropRect.width  / 2,
                    y: dropRect.top  + dropRect.height / 2
                };
            event.draggable.draggable({
                snap: {
                targets: [dropCenter]
                }
            });
            // feedback the possibility of a drop
            dropzoneElement.classList.add('can--catch');
            draggableElement.classList.add('drop--me');
        },
        ondragleave: function (event) {
            // remove the drop feedback style
            event.target.classList.remove('can--catch', 'caught--it');
            event.relatedTarget.classList.remove('drop--me');
            event.target.classList.remove('drop-target');
        },
        ondrop: function (event) {
            event.target.classList.add('caught--it');
            /* ARRIVANTE */
            let arrivante = event.relatedTarget.getAttribute('data-ord');
            let id_from = event.relatedTarget.getAttribute('data-id');
            /* PARTENTE */
            let partente = event.target.firstElementChild.getAttribute('data-ord');
            let id_to = event.target.firstElementChild.getAttribute('data-id');
            /* SELEZIONARE PARENT DI PROVENIENZA */
            let parent = document.querySelector(`.dropzone[data-ord="${event.relatedTarget.getAttribute('data-ord')}"]`);
            parent.appendChild(event.target.firstElementChild);
            parent.removeChild(event.relatedTarget);
            /* SELEZIONARE PARENT DI ARRIVO */
            let target = document.querySelector(`.dropzone[data-ord="${event.target.getAttribute('data-ord')}"]`);
            target.appendChild(event.relatedTarget);
            /* POSIZIONIAMO IL CHILD CHE VA VIA */
            target.style.webkitTransform =
                event.relatedTarget.style.transform =
                    'translate(' + 0 + 'px, ' + 0 + 'px)';
            event.relatedTarget.setAttribute('data-x', 0);
            event.relatedTarget.setAttribute('data-y', 0);
            // aggiornare tutti i data attr
            event.target.firstElementChild.dataset.ord = partente;
            parent.firstElementChild.dataset.ord = arrivante;

            /* RENDIAMO PERSISTENTE */
            body = {
                id_from : id_from,
                id_to : id_to,
                model_name: model_name,
                app: app,
                model_parent: model_parent,
            }
            fetch(djvars.urls.api_sort_model, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'X-CSRFToken': djvars.csrf_token,
                },
                body: JSON.stringify(body)
            })
            .then(resp => resp.json())
            .then(responseData => {
                console.log(responseData.status);

                if (responseData.status == 'success' ) {
                    console.log(responseData.status);
                    // live-ord
                    document.querySelector(`.live-ord[data-id="${responseData.id_from}"]`).innerHTML = responseData.from_ord;
                    document.querySelector(`.live-ord[data-id="${responseData.id_to}"]`).innerHTML = responseData.to_ord;
                } else {
                    console.warn(responseData.message);
                    alert('An Error occurred while saving models');
                }
            })
            .catch(error => {

                alert('An issue with the server has been detected:\n'+error);
            })

        },
        ondropdeactivate: function (event) {
            // remove active dropzone feedback
            event.target.classList.remove('can--drop');
            event.target.classList.remove('can--catch');
            event.target.classList.remove('drop-target');
        }
    });
    }

    function getNodeIndex(node) {
        var index = 0;
        while ( (node = node.previousSibling) ) {
            if (node.nodeType != 3 || !/^\s*$/.test(node.data)) {
            index++;
            }
        }
        return index;
    }

    function eleHasClass(el, cls) {
        return el.className && new RegExp("(\\s|^)" + cls + "(\\s|$)").test(el.className);
    }

    window.onload = function() {
        init();
    }

})();
