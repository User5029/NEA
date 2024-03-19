

class HASHING {
    constructor() {

    }


    async hash(string) {
        let sum = 0
        let tot = 0

        for(const i of string){
            let char = i.charCodeAt(0)
            sum = sum + char
            tot += 1 + 0.01*char

            if(sum === Infinity){
                sum = sum - char
                sum = Math.floor(sum/3)
            }
            if(tot === Infinity){
                tot = tot - char
                tot = Math.floor(tot/356)
            }
        }

        let num = Math.sqrt(sum)*tot*Math.PI
        if(num === Infinity){
            num = Math.sqrt(sum)*Math.sqrt(tot)*0.5
        }
        let slot = num % 52637
        slot = Math.floor(slot)

        return slot
    }
}

module.exports = {HASHING}