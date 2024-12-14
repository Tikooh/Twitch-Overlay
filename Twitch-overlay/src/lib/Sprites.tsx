import noble_woman_Gif from '../images/people/Noble-Woman/Noble-woman-idle.gif'
import noble_woman_walking from '../images/people/Noble-Woman/Noble-woman-walk.gif'
import artistGif from '../images/people/Artist/Artist-idle.gif'
import artistWalking from '../images/people/Artist/Artist-walk.gif'

export const artist = {
    idle: artistGif,
    walk: artistWalking
}

export const nobleWoman = {
    idle: noble_woman_Gif,
    walk: noble_woman_walking
}

export type SpriteType = 'artist' | 'noble_woman'

export const spriteMap: Record<SpriteType, { idle: string; walk: string }> = {
    'artist': artist,
    'noble_woman': nobleWoman
}
