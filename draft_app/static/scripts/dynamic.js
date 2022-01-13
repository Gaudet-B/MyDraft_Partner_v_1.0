
function displayAdvanced(){

    const htmlObject = {
    
        advancedOptions: `<p class="fw-bold fs-5 text-decoration-underline">Starting Roster:</p>
        <form id="form" action="/players/results" method="post" class="form" >
        <input type="hidden" name="league_name" id="hidden_league_name" value="">
        <input type="hidden" name="team_name" id="hidden_team_name" value="">
        <input type="hidden" name="num_of_teams" id="hidden_num_of_teams" value="">
        <input type="hidden" name="draft_position" id="hidden_draft_position" value="">
        <input type="hidden" name="draft_rounds" id="hidden_draft_rounds" value="">
        <div class="d-flex flex-row py-2">
            <label for= "qb_select" class="form-label">QB</label>
            <select name="qb_select" class="form-select mx-3" style="max-width: 75px;">
                <option value="1">1</option>
                <option value="2">2</option>
            </select>
        </div>
        <div class="d-flex flex-row py-2">
            <label for= "rb_select" class="form-label">RB</label>
            <select name="rb_select" class="form-select mx-3" style="max-width: 75px;">
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
            </select>
        </div>
        <div class="d-flex flex-row py-2">
            <label for= "wr_select" class="form-label">WR</label>
            <select name="wr_select" class="form-select mx-3" style="max-width: 75px;">
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
            </select>
        </div>
        <div class="d-flex flex-row py-2">
            <label for= "te_select" class="form-label">TE</label>
            <select name="te_select" class="form-select mx-3" style="max-width: 75px;">
                <option value="1">1</option>
                <option value="2">2</option>
            </select>
        </div>
        <div class="d-flex flex-row py-2">
            <label for= "flex_select" class="form-label">FLEX</label>
            <select name="flex_select" class="form-select mx-3" style="max-width: 75px;">
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
            </select>
        </div>
        <div class="d-flex flex-row pt-3">
            <p class="mx-2">Play <strong>with</strong> a Superflex?</p>
            <input name="super_flex" type="radio" class="form-check-input mx-2" value="true"></input>
            <label for="super_flex" class="form-check-label mx-2">Yes</label>
            <input name="super_flex" type="radio" class="form-check-input mx-2" value="false" checked></input>
            <label for="super_flex" class="form-check-label mx-2">No</label>
        </div>
        <div class="d-flex flex-row pt-3">
            <p class="mx-2">Play <strong>without</strong> Team Defense? (D/ST)</p>
            <input name="no_defenses" type="radio" class="form-check-input mx-2" value="true"></input>
            <label for="no_defenses" class="form-check-label mx-2">Yes</label>
            <input name="no_defenses" type="radio" class="form-check-input mx-2" value="false" checked></input>
            <label for="no_defenses" class="form-check-label mx-2">No</label>
        </div>
        <div class="d-flex flex-row pt-3">
            <p class="mx-2">Play <strong>without</strong> Kickers?</p>
            <input name="no_kickers" type="radio" class="form-check-input mx-2" value="true"></input>
            <label for="no_kickers" class="form-check-label mx-2">Yes</label>
            <input name="no_kickers" type="radio" class="form-check-input mx-2" value="false" checked></input>
            <label for="no_kickers" class="form-check-label mx-2">No</label>
        </div>
        <p class="fw-bold fs-5 text-decoration-underline">Customize Recommendations:</p>
        <p class="fst-italic">If you need a RB in the 1st round, or are more comfortable taking an early QB - this is the place to adjust those serttings.</p>
        <div class="d-flex flex-row pt-3">
            <label for= "rd1_priority" class="form-label">Round One Priority:</label>
            <select name="rd1_priority" class="form-select mx-3" style="max-width: 75px;">
                <option value="-">no preference</option>
                <option value="QB">QB</option>
                <option value="RB">RB</option>
                <option value="WR">WR</option>
                <option value="TE">TE</option>
            </select>
        </div>
        <div class="d-flex flex-row pt-3">
            <label for= "rd2_priority" class="form-label">Round Two Priority:</label>
            <select name="rd2_priority" class="form-select mx-3" style="max-width: 75px;">
                <option value="-">no preference</option>
                <option value="QB">QB</option>
                <option value="RB">RB</option>
                <option value="WR">WR</option>
                <option value="TE">TE</option>
            </select>
        </div>
        <div class="d-flex flex-row pt-3">
            <label for= "rd3_priority" class="form-label">Round Three Priority:</label>
            <select name="rd3_priority" class="form-select mx-3" style="max-width: 75px;">
                <option value="-">no preference</option>
                <option value="QB">QB</option>
                <option value="RB">RB</option>
                <option value="WR">WR</option>
                <option value="TE">TE</option>
            </select>
        </div>
        <div class="d-flex flex-row pt-3">
            <label for= "rd4_priority" class="form-label">Round Four Priority:</label>
            <select name="rd4_priority" class="form-select mx-3" style="max-width: 75px;">
                <option value="-">no preference</option>
                <option value="QB">QB</option>
                <option value="RB">RB</option>
                <option value="WR">WR</option>
                <option value="TE">TE</option>
            </select>
        </div>
        <div class="d-flex flex-row pt-3">
            <label for= "rd5_priority" class="form-label">Round Five Priority:</label>
            <select name="rd5_priority" class="form-select mx-3" style="max-width: 75px;">
                <option value="-">no preference</option>
                <option value="QB">QB</option>
                <option value="RB">RB</option>
                <option value="WR">WR</option>
                <option value="TE">TE</option>
            </select>
        </div>
        <div class="d-flex flex-row pt-3">
            <label for= "rd6_priority" class="form-label">Round Six Priority:</label>
            <select name="rd6_priority" class="form-select mx-3" style="max-width: 75px;">
                <option value="-">no preference</option>
                <option value="QB">QB</option>
                <option value="RB">RB</option>
                <option value="WR">WR</option>
                <option value="TE">TE</option>
            </select>
        </div>
        <div id="target_player_div" class="d-flex flex-column justify-content-evenly mt-3">
            <p class="fw-bold">Do you have a late-round "must have" target player?</p>
            <label for="target_player" id="target_player_label" class="form-label">If so, enter player name here:</label>
            <!-- <input name="target_player" id="target_player_input" type="text" class="form-control" onfocus='autocomplete(this)'> -->
            <input name="target_player" id="target_player_input" type="text" placeholder="(optional)" class="form-control" oninput='autofill(this)'>
        </div>
        <button type="submit" name="submit_btn" id="submit_btn" class="btn btn-primary my-4 fw-bold pt-2" style="max-width: 50px; min-height: 50px;">GO</button>
        </form>`,
        
        advancedOptionsWithScript: `<p class="fw-bold fs-5 text-decoration-underline">Starting Roster:</p>
        <div class="d-flex flex-row py-2">
            <label for= "qb_select" class="form-label">QB</label>
            <select name="qb_select" class="form-select mx-3" style="max-width: 75px;">
                <option value="1">1</option>
                <option value="2">2</option>
            </select>
        </div>
        <div class="d-flex flex-row py-2">
            <label for= "rb_select" class="form-label">RB</label>
            <select name="rb_select" class="form-select mx-3" style="max-width: 75px;">
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
            </select>
        </div>
        <div class="d-flex flex-row py-2">
            <label for= "wr_select" class="form-label">WR</label>
            <select name="wr_select" class="form-select mx-3" style="max-width: 75px;">
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
            </select>
        </div>
        <div class="d-flex flex-row py-2">
            <label for= "te_select" class="form-label">TE</label>
            <select name="te_select" class="form-select mx-3" style="max-width: 75px;">
                <option value="1">1</option>
                <option value="2">2</option>
            </select>
        </div>
        <div class="d-flex flex-row py-2">
            <label for= "flex_select" class="form-label">FLEX</label>
            <select name="flex_select" class="form-select mx-3" style="max-width: 75px;">
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
            </select>
        </div>
        <div class="d-flex flex-row pt-3">
            <p class="mx-2">Play <strong>with</strong> a Superflex?</p>
            <input name="super_flex" type="radio" class="form-check-input mx-2" value="true"></input>
            <label for="super_flex" class="form-check-label mx-2">Yes</label>
            <input name="super_flex" type="radio" class="form-check-input mx-2" value="false" checked></input>
            <label for="super_flex" class="form-check-label mx-2">No</label>
        </div>
        <div class="d-flex flex-row pt-3">
            <p class="mx-2">Play <strong>without</strong> Team Defense? (D/ST)</p>
            <input name="no_defenses" type="radio" class="form-check-input mx-2" value="true"></input>
            <label for="no_defenses" class="form-check-label mx-2">Yes</label>
            <input name="no_defenses" type="radio" class="form-check-input mx-2" value="false" checked></input>
            <label for="no_defenses" class="form-check-label mx-2">No</label>
        </div>
        <div class="d-flex flex-row pt-3">
            <p class="mx-2">Play <strong>without</strong> Kickers?</p>
            <input name="no_kickers" type="radio" class="form-check-input mx-2" value="true"></input>
            <label for="no_kickers" class="form-check-label mx-2">Yes</label>
            <input name="no_kickers" type="radio" class="form-check-input mx-2" value="false" checked></input>
            <label for="no_kickers" class="form-check-label mx-2">No</label>
        </div>
        <p class="fw-bold fs-5 text-decoration-underline">Customize Recommendations:</p>
        <p class="fst-italic">If you need a RB in the 1st round, or are more comfortable taking an early QB - this is the place to adjust those serttings.</p>
        <div class="d-flex flex-row pt-3">
            <label for= "rd1_priority" class="form-label">Round One Priority:</label>
            <select name="rd1_priority" class="form-select mx-3" style="max-width: 75px;">
                <option value="QB">QB</option>
                <option value="RB">RB</option>
                <option value="WR">WR</option>
                <option value="TE">TE</option>
            </select>
        </div>
        <div class="d-flex flex-row pt-3">
            <label for= "rd2_priority" class="form-label">Round Two Priority:</label>
            <select name="rd2_priority" class="form-select mx-3" style="max-width: 75px;">
                <option value="QB">QB</option>
                <option value="RB">RB</option>
                <option value="WR">WR</option>
                <option value="TE">TE</option>
            </select>
        </div>
        <div class="d-flex flex-row pt-3">
            <label for= "rd3_priority" class="form-label">Round Three Priority:</label>
            <select name="rd3_priority" class="form-select mx-3" style="max-width: 75px;">
                <option value="QB">QB</option>
                <option value="RB">RB</option>
                <option value="WR">WR</option>
                <option value="TE">TE</option>
            </select>
        </div>
        <div class="d-flex flex-row pt-3">
            <label for= "rd4_priority" class="form-label">Round Four Priority:</label>
            <select name="rd4_priority" class="form-select mx-3" style="max-width: 75px;">
                <option value="QB">QB</option>
                <option value="RB">RB</option>
                <option value="WR">WR</option>
                <option value="TE">TE</option>
            </select>
        </div>
        <div class="d-flex flex-row pt-3">
            <label for= "rd5_priority" class="form-label">Round Five Priority:</label>
            <select name="rd5_priority" class="form-select mx-3" style="max-width: 75px;">
                <option value="QB">QB</option>
                <option value="RB">RB</option>
                <option value="WR">WR</option>
                <option value="TE">TE</option>
            </select>
        </div>
        <div class="d-flex flex-row pt-3">
            <label for= "rd6_priority" class="form-label">Round Six Priority:</label>
            <select name="rd6_priority" class="form-select mx-3" style="max-width: 75px;">
                <option value="QB">QB</option>
                <option value="RB">RB</option>
                <option value="WR">WR</option>
                <option value="TE">TE</option>
            </select>
        </div>
        <div id="target_player_div" class="d-flex flex-column justify-content-evenly mt-3">
            <p class="fw-bold">Do you have a late-round "must have" target player?</p>
            <label for="target_player" id="target_player_label" class="form-label">If so, enter player name here:</label>
            <!-- <input name="target_player" id="target_player_input" type="text" class="form-control" onfocus='autocomplete(this)'> -->
            <input name="target_player" id="target_player_input" type="text" placeholder="(optional)" class="form-control" oninput='autofill(this)'>
        </div>
        <button type="submit" name="submit_btn" id="submit_btn" class="btn btn-primary my-4 fw-bold pt-2" style="max-width: 50px; min-height: 50px;">GO</button>
        <script type="text/javascript">
            
            var names = {{ player_names|safe }}
        
            const addActive = (elem, current) => {
        
                removeActive(elem)
        
                if (current >= elem.childNodes.length) current = 0
                if (current < 0) current = elem.childNodes.length - 1
        
                elem.childNodes[current].classList.add("autocomplete-active")
            }
        
            const removeActive = elem => {
                for (let i = 0; i < elem.childNodes.length; i++) {
                    elem.childNodes[i].classList.remove("autocomplete-active")
                }
            }
        
            const handleClick = e => {
                document.getElementById("target_player_input").value = e.innerHTML
                closeList()
            }
        
            const select = e => {
        
                let playerList = document.getElementById("autocomplete-list")
                console.log(playerList)
                let current = -1
                
                if (e.keyCode === 40) {
                    e.preventDefault()
                    current++
                    addActive(playerList, current)
                } else if (e.keyCode === 38) {
                    e.preventDefault()
                    current--
                    addActive(playerList, current)
                } else if (e.keyCode === 13) {
                    e.preventDefault()
                    if (current > -1) {
                        document.getElementById("target_player_input").value = playerList.childNodes[current].innerHTML
                    }
                } 
            }
        
            const closeList = () => {
                let delList = document.getElementById("autocomplete-list")
                // console.log(delList)
                delList.innerHTML = ""
            }
        
            const autofill = (element, namesArr = names) => {
                
                // console.log(namesArr)
                let prefix = element.value
                // console.log(prefix)
        
                class TrieNode {
                    constructor(value) {
                        this.value = value
                        this.children = {}
                        this.isEndOfWord = false
                        this.word = ""
                    }
                }
        
                class Trie {
        
                    constructor() {
                        this.root = new TrieNode(null)
                    }
        
                    addName(string) {
                        // console.log(string)
                        let currentNode = this.root
                        // console.log(currentNode)
                        for (let char of string) {
                            if (currentNode.children[char] === undefined) {
                                currentNode.children[char] = new TrieNode(char)
                            }
                            currentNode = currentNode.children[char]
                        }
                        currentNode.isEndOfWord = true
                        currentNode.word = string
                    }
        
                    search(string) {
                        let currentNode = this.root
                        for (let char of string) {
                            if (currentNode.children[char] === undefined) {
                                return false
                            }
                            currentNode = currentNode.children[char]
                        }
                        return currentNode.isEndOfWord
                    }
        
                    // auto(string) {
                    //     let word = ""
                    //     for (let char of string) {
                    //         if (currentNode.children[char] === undefined) {
        
                    //         }
        
                    //     }
                    // }
        
                    namesWithPrefix(prefix) {
        
                        // console.log(prefix)
        
                        let currentNode = this.root
                        // console.log(currentNode)
                        let arrayOfNames = []
        
                        const getAllNames = (root, namesArr) => {
                            // let name = prefix
                            // console.log(name)
                            // console.log(root)
                            if (root.isEndOfWord) {
                                namesArr.push(root.word)
                                // name = ""
                                // console.log(namesArr)
                            } else {
                                for (const char in root.children) {
                                    // console.log(char)
                                    // name += char
                                    // console.log(root.children[char])
                                    getAllNames(root.children[char], namesArr)
                                }
                            }
                        }
        
                        for (const char of prefix) {
                            // console.log(char)
                            // console.log(Object.keys(currentNode.children))
                            if (Object.keys(currentNode.children).includes(char)) {
                                currentNode = currentNode.children[char]
                                // console.log(currentNode)
                            } else return arrayOfNames
                        }
        
                        getAllNames(currentNode, arrayOfNames)
        
                        // console.log(arrayOfNames)
                        return arrayOfNames
        
                    }
        
                }
        
                if (prefix.length < 1) {
                    console.log(prefix.length)
                    closeList()
                    return
                }
        
                let newTrie = new Trie()
        
                for (let i = 0; i < namesArr.length; i++) {
                    // console.log(namesArr[i])
                    newTrie.addName(namesArr[i])
                }
        
                if (!document.getElementById("autocomplete-list")) {
                    let listContainer = document.createElement("div")
                    let targetDiv = document.getElementById("target_player_div")
        
                    listContainer.setAttribute("id", "autocomplete-list")
                    listContainer.setAttribute("class", "d-flex flex-column autocomplete-items")
                    // listContainer.addEventListener("keydown", select(this))
        
                    targetDiv.appendChild(listContainer)
        
                } else {
                    
                    if (document.getElementById("autocomplete-list").childNodes.length > 0) {
                        closeList()
                    }
        
                    let listContainer = document.getElementById("autocomplete-list")
                    let autocompleteList = newTrie.namesWithPrefix(prefix)
        
                    listContainer.innerHTML = ""
        
                    for (let i = 0; i < autocompleteList.length; i++) {
                        listContainer.innerHTML += '<div onclick='handleClick(this)' class="autocomplete-item">/$/{autocompleteList[i]}</div>'
                    }
        
                }
                // console.log(newTrie)
                // console.log(newTrie.namesWithPrefix(prefix))
                return newTrie.namesWithPrefix(prefix)
        
            }
        </script>`,
    
        scriptText: `const autofill = (element, namesArr) => {
            console.log("BEGIN");
            let prefix = element.value;
            class TrieNode {
                constructor(value) {
                    this.value = value;
                    this.children = {};
                    this.isEndOfWord = false;
                };
            };
            class Trie {
                constructor() {
                    this.root = new TrieNode(null);
                };
                addName(string) {
                    let currentNode = this.root;
                    for (let char of string) {
                        if (currentNode.children[char] === undefined) {
                            currentNode.children[char] = new TrieNode(char);
                        };
                        currentNode = currentNode.children[char];
                    };
                    currentNode.isEndOfWord = true;
                };
                search(string) {
                    let currentNode = this.root;
                    for (let char of string) {
                        if (currentNode.children[char] === undefined) {
                            return false;
                        };
                        currentNode = currentNode.children[char];
                    };
                    return currentNode.isEndOfWord;
                };
                // auto(string) {
                //     let word = "";
                //     for (let char of string) {
                //         if (currentNode.children[char] === undefined) {
                //         };
                //     };
                // };
                namesWithPrefix(prefix) {
                    const getAllNames = (root, prefix, namesArr) => {
                        let name = prefix;
                        if (root.isEndOfWord) {
                            namesArr.push(prefix);
                        } else {
                            for (const node in root.children) {
                                name += node.value;
                                getAllNames(node, name, namesArr);
                            };
                        };
                    };
                    let currentNode = this.root;
                    let namesArr = [];
                    for (const char of prefix) {
                        if (!(char in currentNode.children)) return namesArr;
                        currentNode = currentNode[char];
                    };
                    getAllNames(currentNode, prefix, namesArr);
                    return namesArr;
                };
            };
            let newTrie = new Trie;
            for (const name in namesArr) {
                newTrie.addName(name);
            };
            return newTrie.namesWithPrefix(prefix);
        };`
    
    }

    // let text = htmlObject.scriptText
    // let html = htmlObject.advancedOptionsWithScript
    let html = htmlObject.advancedOptions
    let container = document.getElementById("advanced_container")
    let image = document.getElementById("arrow")

    // console.log(container.innerHTML.length)x
    
    if (container.innerHTML.length > 5000) {

        // let newButton = document.createElement("button")
        let delScript = document.getElementById("autocomplete-script")

        container.classList.remove("p-4")
        container.innerHTML = ""

        // newButton.setAttribute("name", "submit_btn")
        // newButton.setAttribute("id", "submit_btn")
        // newButton.setAttribute("class", "btn btn-primary my-4 fw-bold")
        // newButton.innerHTML = "GO"

        if (delScript) delScript.remove()
        
        // document.getElementById("form").appendChild(newButton)
        document.getElementById("arrow").src = "/static/assets/down-arrow-icon-vector.png"
        
    } else {

        let button = document.getElementById("submit_btn")
        if (button) button.remove()
        // setTimeout(() => {
        //     document.getElementById("advanced-container").appendChild(button)
        // }, 500);
        container.appendChild(button)
        
        // let script = document.createElement("script")
        // script.id = "autocomplete-script"
        // script.src = "/static/scripts/autocomplete.js"
        // script.type = "text/javascript"
        // script.innerText = text
        // document.body.appendChild(script)

        container.classList.add("p-4")
        container.innerHTML = html

        document.getElementById("arrow").src = "/static/assets/up-arrow-icon-vector.png"

        let league = document.getElementById("league_name_input").value
        document.getElementById("hidden_league_name").value = league

        let team = document.getElementById("team_name_input").value
        document.getElementById("hidden_team_name").value = team

        let numTeams = document.getElementById("num_of_teams_select").value
        document.getElementById("hidden_num_of_teams").value = numTeams

        let position = document.getElementById("draft_position_select").value
        document.getElementById("hidden_draft_position").value = position

        let rounds = document.getElementById("draft_rounds_select").value
        document.getElementById("hidden_draft_rounds").value = rounds


    }
}

function mousePointer(element){
    element.style.cursor = "pointer";
}

const autocomplete = e => {
    console.log("confirm")
    console.log(e.id);
}