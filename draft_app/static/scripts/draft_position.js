const draftOrder = (teams, spot, rounds) => {
  let arr = []
  let round = 1
  let pick = 0
  for (let j = 1; j <= rounds; j++) {
    if (round % 2 != 0) {
      for (let i = 1; i <= teams; i++) {
        pick++
        if (i == spot) {
          arr.push(pick)
        }
      }
      console.log(round)
    } else if (round % 2 == 0) {
      for (let i = teams; i > 0; i--) {
        pick++
        if (i == spot) {
          arr.push(pick)
        }
      }
      console.log(round)
    }
    round++
  }
  return arr
}

const displaySpots = () => {
  max = document.getElementById('num_of_teams_select').value
  options = document.getElementById('draft_position_select')
  options.innerHTML = `<option>-</option>`
  for (let i = 1; i <= max; i++) {
    options.innerHTML += `<option value="${i}">${i}</option>`
  }
  return max
}

console.log(draftOrder(12, 8, 16))
