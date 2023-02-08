

class BoggleGame {
    constructor(boardId, secs = 60) {
        this.secs = secs
        this.showTimer();
        this.score = 0
        this.words = new Set();
        this.board = $('.' + boardId);

        this.timer = setInterval(this.time.bind(this), 1000)

        $(".add-word", this.board).on("submit", this.handleSubmit.bind(this));
    }

    addWordToList(word) {
        $('.words', this.board).append($("<li>", { text: word }))
    }

    showmsg(msg, status) {
        $('.msg', this.board).text(msg).removeClass().addClass(`msg ${status}`);
    }

    showTimer() {
        $('.timer', this.board).text(this.secs)
    }

    showscore() {
        $('.score', this.board).text(this.score)
    }

    async handleSubmit(evt) {
        evt.preventDefault();
        const $word = $('.word', this.board);

        let word = $word.val();
        if (!word) {
            this.showmsg("Submit a word you have found", 'err')
            return;
        }
        if (this.words.has(word)) {
            this.showmsg(`${word} has already been found`, 'err')
            return;
        }

        const resp = await axios.get("/check-word", { params: { word: word } });
        console.log(resp)
        if (resp.data.result === "not-on-board") {
            this.showmsg(`${word} is not in the board`, 'err')
        }
        else if (resp.data.result === "not-word") {
            this.showmsg(`${word} is not a word`, 'err')
        }
        else {
            this.addWordToList(word)
            this.words.add(word)
            this.showmsg(`Added: ${word}`, 'ok')
            this.score += word.length
            this.showscore()
        }
        $word.val('').focus();
    }

    async time() {
        this.secs -= 1
        this.showTimer()

        if (this.secs === 0) {
            clearInterval(this.timer)
            await this.gameOver()
        }
    }

    async gameOver() {
        $('.add-word', this.board).hide();
        const resp = await axios.post('/post-score', { score: this.score })
        if (resp.data.broken_record) {
            this.showmsg(`New record: ${this.score}`, 'ok')
        }
        else {
            this.showmsg(`Final score: ${this.score}`, 'ok')
        }
    }
}

let game = new BoggleGame('boggle');