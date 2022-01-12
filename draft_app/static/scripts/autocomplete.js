
const autofill = (element, namesArr = namesArr) => {
    
    console.log("BEGIN")
    
    let prefix = element.value

    class TrieNode {
        constructor(value) {
            this.value = value
            this.children = {}
            this.isEndOfWord = false
        }
    }

    class Trie {

        constructor() {
            this.root = new TrieNode(null)
        }

        addName(string) {
            let currentNode = this.root
            for (let char of string) {
                if (currentNode.children[char] === undefined) {
                    currentNode.children[char] = new TrieNode(char)
                }
                currentNode = currentNode.children[char]
            }
            currentNode.isEndOfWord = true
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

            const getAllNames = (root, prefix, namesArr) => {
                let name = prefix
                if (root.isEndOfWord) {
                    namesArr.push(prefix)
                } else {
                    for (const node in root.children) {
                        name += node.value
                        getAllNames(node, name, namesArr)
                    }
                }
            }

            let currentNode = this.root
            let namesArr = []

            for (const char of prefix) {
                if (!(char in currentNode.children)) return namesArr
                currentNode = currentNode[char]
            }

            getAllNames(currentNode, prefix, namesArr)

            return namesArr

        }

    }

    let newTrie = new Trie

    for (const name in namesArr) {
        newTrie.addName(name)
    }

    return newTrie.namesWithPrefix(prefix)

}