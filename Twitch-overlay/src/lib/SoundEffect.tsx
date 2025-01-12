import Engineer from '../SoundEffects/Engineer.mp3'

export const playSound = () => {
    const audio = new Audio(Engineer)
    audio.play()
    console.log("playing sound")
}
