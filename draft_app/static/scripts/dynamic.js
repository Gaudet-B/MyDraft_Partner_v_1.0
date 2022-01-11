const htmlObject = {
    advancedOptions: '<p class="fw-bold fs-5 text-decoration-underline">Starting Roster:</p><div class="d-flex flex-row py-2"><label for= "qb_select" class="form-label">QB</label><select name="qb_select" class="form-select mx-3" style="max-width: 75px;"><option value="1">1</option><option value="2">2</option></select></div><div class="d-flex flex-row py-2"><label for= "rb_select" class="form-label">RB</label><select name="rb_select" class="form-select mx-3" style="max-width: 75px;"><option value="1">1</option><option value="2">2</option><option value="3">3</option></select></div><div class="d-flex flex-row py-2"><label for= "wr_select" class="form-label">WR</label><select name="wr_select" class="form-select mx-3" style="max-width: 75px;"><option value="1">1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option></select></div><div class="d-flex flex-row py-2"><label for= "te_select" class="form-label">TE</label><select name="te_select" class="form-select mx-3" style="max-width: 75px;"><option value="1">1</option><option value="2">2</option></select></div><div class="d-flex flex-row py-2"><label for= "flex_select" class="form-label">FLEX</label><select name="flex_select" class="form-select mx-3" style="max-width: 75px;"><option value="1">1</option><option value="2">2</option><option value="3">3</option></select></div><div class="d-flex flex-row pt-3"><p class="mx-2">SUPER FLEX?</p><input name="super_yes" type="radio" class="form-check-input mx-2" value="y"></input><label for="super_yes" class="form-check-label mx-2">Yes</label><input name="super_no" type="radio" class="form-check-input mx-2" value="n" checked></input><label for="super_no" class="form-check-label mx-2">No</label></div><div class="d-flex flex-row pt-3"><p class="mx-2">DEFENSE?</p><input name="defense_yes" type="radio" class="form-check-input mx-2" value="y"></input><label for="defense_yes" class="form-check-label mx-2">Yes</label><input name="defense_no" type="radio" class="form-check-input mx-2" value="n" checked></input><label for="defense_no" class="form-check-label mx-2">No</label></div><div class="d-flex flex-row pt-3"><p class="mx-2">KICKER?</p><input name="kicker_yes" type="radio" class="form-check-input mx-2" value="y"></input><label for="kicker_yes" class="form-check-label mx-2">Yes</label><input name="kicker_no" type="radio" class="form-check-input mx-2" value="n" checked></input><label for="kicker_no" class="form-check-label mx-2">No</label></div><p class="fw-bold fs-5 text-decoration-underline">Customize Recommendations:</p><p class="fst-italic">If you need a RB in the 1st round, or are more comfortable taking an early QB - this is the place to adjust those serttings.</p><div class="d-flex flex-row pt-3"><label for= "rd1_priority" class="form-label">Round One Priority:</label><select name="rd1_priority" class="form-select mx-3" style="max-width: 75px;"><option value="QB">QB</option><option value="RB">RB</option><option value="WR">WR</option><option value="TE">TE</option></select></div><div class="d-flex flex-row pt-3"><label for= "rd2_priority" class="form-label">Round Two Priority:</label><select name="rd2_priority" class="form-select mx-3" style="max-width: 75px;"><option value="QB">QB</option><option value="RB">RB</option><option value="WR">WR</option><option value="TE">TE</option></select></div><div class="d-flex flex-row pt-3"><label for= "rd3_priority" class="form-label">Round Three Priority:</label><select name="rd3_priority" class="form-select mx-3" style="max-width: 75px;"><option value="QB">QB</option><option value="RB">RB</option><option value="WR">WR</option><option value="TE">TE</option></select></div><div class="d-flex flex-row pt-3"><label for= "rd4_priority" class="form-label">Round Four Priority:</label><select name="rd4_priority" class="form-select mx-3" style="max-width: 75px;"><option value="QB">QB</option><option value="RB">RB</option><option value="WR">WR</option><option value="TE">TE</option></select></div><div class="d-flex flex-row pt-3"><label for= "rd5_priority" class="form-label">Round Five Priority:</label><select name="rd5_priority" class="form-select mx-3" style="max-width: 75px;"><option value="QB">QB</option><option value="RB">RB</option><option value="WR">WR</option><option value="TE">TE</option></select></div><div class="d-flex flex-row pt-3"><label for= "rd6_priority" class="form-label">Round Six Priority:</label><select name="rd6_priority" class="form-select mx-3" style="max-width: 75px;"><option value="QB">QB</option><option value="RB">RB</option><option value="WR">WR</option><option value="TE">TE</option></select></div><div class="d-flex flex-column justify-content-evenly mt-3"><p class="fw-bold">Do you have a late-round "must have" target player?</p><label for="target_player" id="target_player_label" class="form-label">If so, enter player name here:</label><input type="text" name="target_player" id="target_player_input" placeholder="(optional)" class="form-control"></div><button type="submit" name="submit_btn" id="submit_btn" class="btn btn-primary my-4 fw-bold pt-2" style="max-width: 50px;">GO</button>'
}

function displayAdvanced(){

    let html = htmlObject.advancedOptions;
    let container = document.getElementById("advanced_container");
    let image = document.getElementById("arrow");

    console.log(container.innerHTML.length)
    
    if (container.innerHTML.length > 5000) {

        let newButton = document.createElement("button");

        container.classList.remove("p-4");
        container.innerHTML = "";
        newButton.setAttribute("name", "submit_btn");
        newButton.setAttribute("id", "submit_btn");
        newButton.setAttribute("class", "btn btn-primary my-4 fw-bold");
        newButton.innerHTML = "GO"
        
        document.getElementById("form").appendChild(newButton);
        document.getElementById("arrow").src = "/static/assets/down-arrow-icon-vector.png";
        
    } else {

        let button = document.getElementById("submit_btn");

        button.remove()
        container.classList.add("p-4");
        container.innerHTML = html;

        document.getElementById("arrow").src = "/static/assets/up-arrow-icon-vector.png";

    }
}

function mousePointer(element){
    element.style.cursor = "pointer";
}