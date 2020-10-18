document.addEventListener("DOMContentLoaded", () => {

    fetch("/change_followers")
    .then(response => response.json())
    .then(list_following => {
        var list_following = JSON.stringify(list_following);
        localStorage.setItem('list_following', list_following)
    })

    if(list_following.includes(profile_name) === false){
        document.querySelector("#fol_unfol").innerHTML = "Follow";
    }
    else{
        document.querySelector("#fol_unfol").innerHTML = "Unfollow";
    }

    document.querySelector("#fol_unfol").onclick = () => {

        // Algorithm: Get latest list of ppl the logged in user is following,
        // Check if the clicked profile_name (set in the profile.html template) is in this list using the includes function
        // If it isn't, that user is not yet being followed. Set the button to say "unfollow and send a change via post to server to change the num of followers by "1"
        // Use setTimout function to run another fetch call to GET the now updated list of ppl the logged in user is following
        fetch("/change_followers")
        .then(response => response.json())
        .then(data => {
            var list_following = JSON.stringify(data);
            localStorage.setItem('list_following', list_following)


            if(list_following.includes(profile_name) === false){
                document.querySelector("#fol_unfol").innerHTML = "Unfollow";
                fetch("/change_followers", {
                    method: "POST",
                    body: JSON.stringify({
                        num_fol_change: 1,
                        profile_name: profile_name
                    })
                })
                setTimeout(chg_followers, 20);
            }

            else{
                document.querySelector("#fol_unfol").innerHTML = "Follow";
                fetch("/change_followers", {
                    method: "POST",
                    body: JSON.stringify({
                        num_fol_change: -1,
                        profile_name: profile_name
                    })
                })
                setTimeout(chg_followers, 20);
            }
        })

        // call back function which gets the Count of number of followers via a fetch call after 20milliseconds on running the setTimout function above
        function chg_followers(){
            fetch("/change_followers")
            .then(response => response.json())
            .then(data => {
                var num_of_followers = data["num_of_followers"]
                document.querySelector("#num_followers").innerHTML = num_of_followers;
            })
        }
    }
})