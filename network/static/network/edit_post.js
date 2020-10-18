//2 Javascript functions created. The 1st to enable edit button edit a users posts,  the 2nd to allow a user to like a post.
document.addEventListener("DOMContentLoaded", () => {

    //----------------------------------------------------------------
    // Javascript to enable the editing of a post asynchronously on clicking the "Edit" button
    document.querySelectorAll('.edit_button').forEach(edit_button => {
    edit_button.addEventListener("click", () => {

        //  Get a clicked posts' "post id" using the adjacent property ("previousSibling") of the "Edit" button
        var x = edit_button.previousSibling.id
        fetch("/post/" + x)
        .then(response => response.json())
        .then(post => {

            // Create an editable "textarea" field.
            // Pre-populate this created textare field with previous text data ("post.post") from fetch server call
            // Clear the previous field of older data
            // Append the new pre-populated field to an adjacent div using "nextSibling" property
            // Change the Edit button text to its converse (either "Save" or "Edit") depending on previous actions
            if(edit_button.innerHTML == "Edit"){
                var y = post;
                var z = document.createElement("textarea");
                z.setAttribute("id", "txt")
                z.innerHTML = post.post
                document.getElementById(x).innerHTML = ""
                edit_button.nextSibling.append(z)
                edit_button.innerHTML = "Save"
            }

            else if (edit_button.innerHTML == "Save"){
                fetch("/post/" + x, {
                    method: "POST",
                    body: JSON.stringify({
                        post: document.querySelector("#txt").value
                    })

                })
                document.getElementById(x).innerHTML = document.querySelector("#txt").value
                edit_button.innerHTML = "Edit"
                edit_button.nextSibling.innerHTML = ""
            }
        })
        })
        })


    //----------------------------------------------------------------
    // Javascript to add to count of Likes asynchronously on clicking the like button

    document.querySelectorAll('.like_link').forEach(like_link => {

        //  Get the like link id(ll_id) on clicking a like_link button
        var ll_id = like_link.id

        ll_id_num = ll_id.slice(2)

        fetch("/likes/" + ll_id_num)
            .then(response => response.json())
            .then(initial => {

                var like_status = initial["data"].toString()
                if(like_status == "false"){
                    document.getElementById(ll_id).innerHTML = "Like";
                }
                else{
                    document.getElementById(ll_id).innerHTML = "Unlike";
                }
            })

        like_link.addEventListener("click", () => {
            //  Get the like link id("lk{{post.id}}") on clicking a like_link button. Save as variable ll_id(like link id)
            var ll_id = like_link.id

            // Get the like count id("cnt{{post.id}}") using the adjacent property ("previousSibling") of the like_link button.
            // Save as a variable lcnt_id
            var lcnt_id = like_link.previousSibling.id

            // Get the post id number from the previously concatenated string "lk{{post.id}}" named in the html template by slicing.
            // Save as a variable ll_id_num
            ll_id_num = ll_id.slice(2)

            //----------GET

            fetch("/likes/" + ll_id_num)
            .then(response => response.json())
            .then(status => {

                var status_str = status["data"].toString()
                if(status_str == "false"){
                    // ----------POST Request
                    fetch("/likes/" + ll_id_num, {
                        method: "POST",
                        body: JSON.stringify({
                            "status": true
                        })
                    })
                    document.getElementById(ll_id).innerHTML = "Unlike";
                    // Timer callback function to call a fetch function, in order to get the latest "like" data from the server
                    setTimeout(update, 20);
                }


                else{
                    //--------POST Request
                    fetch("/likes/" + ll_id_num, {
                        method: "POST",
                        body: JSON.stringify({
                            "status": false
                        })
                    })
                 document.getElementById(ll_id).innerHTML = "Like";
                setTimeout(update,20);
                }

                })

            // call back function which gets the Count of likes via a fetch call on running the setTimout function above
            function update(){
                fetch("/likes/" + ll_id_num)
                .then(response => response.json())
                .then(data => {
                    var m = data["count"]
                    document.getElementById(lcnt_id).innerHTML = m;
                })
            }

        })
    })
})
