import logging
import os
import nltk

from nltk.corpus import stopwords
from collections import Counter
from pybloom_live import BloomFilter

log = logging.getLogger(__name__)

bad_words = ['fucked', 'brunette', 'erotica', 'fucks', 'teens', 'interracial', 'creampie', 'blowjob', 'nuru massage',
             'latina', 'licking', 'sucking', 'redhead', 'ebony', 'cumshot', 'gangbang', 'slippery', 'squirting',
             'seduces', 'masturbating', 'passionate', 'penetration', 'homemade', 'housewife', 'fetish', 'dildos',
             'masturbation', 'painful', 'milfs', 'pounded', 'licked', 'blondie', 'fingered', 'virgin', 'pussies',
             'foursome', 'swingers', 'bitches', 'throat', 'sextape', 'pregnant', 'perverted', 'exotic', 'malkova',
             '2g1c', '2 girls 1 cup', 'acrotomophilia', 'anal', 'anilingus', 'anus', 'arsehole', 'ass', 'asshole',
             'assmunch', 'auto erotic', 'autoerotic', 'babeland', 'baby batter', 'ball gag', 'ball gravy',
             'ball kicking', 'ball licking', 'ball sack', 'ball sucking', 'bangbros', 'bareback', 'barely legal',
             'barenaked', 'bastardo', 'bastinado', 'bbw', 'bdsm', 'beaver cleaver', 'beaver lips', 'bestiality',
             'bi curious', 'big black', 'big breasts', 'big knockers', 'big tits', 'bimbos', 'birdlock', 'bitch',
             'black cock', 'blonde action', 'blonde on blonde action', 'blow j', 'blow your l', 'blue waffle',
             'blumpkin', 'bollocks', 'bondage', 'boner', 'boob', 'boobs', 'booty call', 'brown showers',
             'brunette action', 'bukkake', 'bulldyke', 'bullet vibe', 'bung hole', 'bunghole', 'busty', 'butt',
             'buttcheeks', 'butthole', 'camel toe', 'camgirl', 'camslut', 'camwhore', 'carpet muncher', 'carpetmuncher',
             'chocolate rosebuds', 'circlejerk', 'cleveland steamer', 'clit', 'clitoris', 'clover clamps',
             'clusterfuck', 'cock', 'cocks', 'coprolagnia', 'coprophilia', 'cornhole', 'cum', 'cumming', 'cunnilingus',
             'cunt', 'darkie', 'date rape', 'daterape', 'deep throat', 'deepthroat', 'dick', 'dildo', 'dirty pillows',
             'dirty sanchez', 'dog style', 'doggie style', 'doggiestyle', 'doggy style', 'doggystyle', 'dolcett',
             'domination', 'dominatrix', 'dommes', 'donkey punch', 'double dong', 'double penetration', 'dp action',
             'eat my ass', 'ecchi', 'ejaculation', 'erotic', 'erotism', 'escort', 'ethical slut', 'eunuch', 'faggot',
             'fecal', 'felch', 'fellatio', 'feltch', 'female squirting', 'femdom', 'figging', 'fingering', 'fisting',
             'foot fetish', 'footjob', 'frotting', 'fuck', 'fucking', 'fuck buttons', 'fudge packer', 'fudgepacker',
             'futanari', 'g-spot', 'gang bang', 'gay sex', 'genitals', 'giant cock', 'girl on', 'girl on top',
             'girls gone wild', 'goatcx', 'goatse', 'gokkun', 'golden shower', 'goo girl', 'goodpoop', 'goregasm',
             'grope', 'group sex', 'guro', 'hand job', 'handjob', 'hard core', 'hardcore', 'hentai', 'homoerotic',
             'honkey', 'hooker', 'hot chick', 'how to kill', 'how to murder', 'huge fat', 'humping', 'incest',
             'intercourse', 'jack off', 'jail bait', 'jailbait', 'jerk off', 'jigaboo', 'jiggaboo', 'jiggerboo', 'jizz',
             'juggs', 'kike', 'kinbaku', 'kinkster', 'kinky', 'knobbing', 'leather restraint',
             'leather straight jacket', 'lemon party', 'lolita', 'lovemaking', 'make me come', 'male squirting',
             'masturbate', 'menage a trois', 'milf', 'missionary position', 'motherfucker', 'mound of venus',
             'mr hands', 'muff diver', 'muffdiving', 'nambla', 'nawashi', 'negro', 'neonazi', 'nig nog', 'nigga',
             'nigger', 'nimphomania', 'nipple', 'nipples', 'nsfw images', 'nude', 'nudity', 'nympho', 'nymphomania',
             'octopussy', 'omorashi', 'one cup two girls', 'one guy one jar', 'orgasm', 'orgy', 'paedophile', 'panties',
             'panty', 'pedobear', 'pedophile', 'pegging', 'penis', 'phone sex', 'piece of shit', 'piss pig', 'pissing',
             'pisspig', 'playboy', 'pleasure chest', 'pole smoker', 'ponyplay', 'poof', 'poop chute', 'poopchute',
             'porn', 'porno', 'pornography', 'prince albert piercing', 'pthc', 'pubes', 'pussy', 'queaf', 'raghead',
             'raging boner', 'rape', 'raping', 'rapist', 'rectum', 'reverse cowgirl', 'rimjob', 'rimming', 'rosy palm',
             'rosy palm and her 5 sisters', 'rusty trombone', 's&m', 'sadism', 'scat', 'schlong', 'scissoring', 'semen',
             'sex', 'sexo', 'sexy', 'shaved beaver', 'shaved pussy', 'shemale', 'shibari', 'shit', 'shota', 'shrimping',
             'slanteye', 'slut', 'smut', 'snatch', 'snowballing', 'sodomize', 'sodomy', 'spic', 'spooge', 'spread legs',
             'strap on', 'strapon', 'strappado', 'strip club', 'style doggy', 'suck', 'sucks', 'suicide girls',
             'sultry women', 'swastika', 'swinger', 'tainted love', 'taste my', 'tea bagging', 'threesome', 'throating',
             'tied up', 'tight white', 'tit', 'tits', 'titties', 'titty', 'tongue in a', 'topless', 'tosser',
             'towelhead', 'tranny', 'tribadism', 'tub girl', 'tubgirl', 'tushy', 'twat', 'twink', 'twinkie',
             'two girls one cup', 'undressing', 'upskirt', 'urethra play', 'urophilia', 'vagina', 'venus mound',
             'vibrator', 'violet blue', 'violet wand', 'vorarephilia', 'voyeur', 'vulva', 'wank', 'wet dream',
             'wetback', 'white power', 'women rapping', 'wrapping men', 'wrinkled starfish', 'xx', 'xxx', 'yaoi',
             'yellow showers', 'yiffy', 'zoophilia', '4r5e', '5h1t', '5hit', 'a55', 'ar5e', 'arrse', 'arse',
             'ass-fucker', 'asses', 'assfucker', 'assfukka', 'assholes', 'asswhole', 'a_s_s', 'b!tch', 'b00bs', 'b17ch',
             'b1tch', 'ballbag', 'balls', 'ballsack', 'bastard', 'beastial', 'beastiality', 'bellend', 'bestial',
             'bi+ch', 'biatch', 'bitcher', 'bitchers', 'bitchin', 'bitching', 'bloody', 'blow job', 'blowjobs',
             'boiolas', 'bollock', 'bollok', 'booobs', 'boooobs', 'booooobs', 'booooooobs', 'breasts', 'buceta',
             'bugger', 'bum', 'bunny fucker', 'buttmuch', 'buttplug', 'c0ck', 'c0cksucker', 'cawk', 'chink', 'cipa',
             'cl1t', 'clits', 'cnut', 'cock-sucker', 'cockface', 'cockhead', 'cockmunch', 'cockmuncher', 'cocksuck ',
             'cocksucked ', 'cocksucker', 'cocksucking', 'cocksucks ', 'cocksuka', 'cocksukka', 'cok', 'cokmuncher',
             'coksucka', 'coon', 'cox', 'crap', 'cummer', 'cums', 'cunilingus', 'cunillingus', 'cuntlick ',
             'cuntlicker ', 'cuntlicking ', 'cunts', 'cyalis', 'cyberfuc', 'cyberfuck ', 'cyberfucked ', 'cyberfucker',
             'cyberfuckers', 'cyberfucking ', 'd1ck', 'damn', 'dickhead', 'dink', 'dinks', 'dirsa', 'dlck',
             'dog-fucker', 'doggin', 'dogging', 'donkeyribber', 'doosh', 'duche', 'dyke', 'ejaculate', 'ejaculated',
             'ejaculates ', 'ejaculating ', 'ejaculatings', 'ejakulate', 'f u c k', 'f u c k e r', 'f4nny', 'fag',
             'fagging', 'faggitt', 'faggs', 'fagot', 'fagots', 'fags', 'fanny', 'fannyflaps', 'fannyfucker', 'fanyy',
             'fatass', 'fcuk', 'fcuker', 'fcuking', 'feck', 'fecker', 'felching', 'fellate', 'fingerfuck ',
             'fingerfucked ', 'fingerfucker ', 'fingerfuckers', 'fingerfucking ', 'fingerfucks ', 'fistfuck',
             'fistfucked ', 'fistfucker ', 'fistfuckers ', 'fistfucking ', 'fistfuckings ', 'fistfucks ', 'flange',
             'fook', 'fooker', 'fucka', 'fucker', 'fuckers', 'fuckhead', 'fuckheads', 'fuckin', 'fuckings',
             'fuckingshitmotherfucker', 'fuckme ', 'fuckwhit', 'fuckwit', 'fuk', 'fuker', 'fukker', 'fukkin', 'fuks',
             'fukwhit', 'fukwit', 'fux', 'fux0r', 'f_u_c_k', 'gangbanged ', 'gangbangs ', 'gaylord', 'gaysex',
             'god-dam', 'god-damned', 'goddamn', 'goddamned', 'hardcoresex ', 'hell', 'heshe', 'hoar', 'hoare', 'hoer',
             'homo', 'hore', 'horniest', 'horny', 'hotsex', 'jack-off ', 'jackoff', 'jap', 'jerk-off ', 'jism', 'jiz ',
             'jizm ', 'kawk', 'knob', 'knobead', 'knobed', 'knobend', 'knobhead', 'knobjocky', 'knobjokey', 'kock',
             'kondum', 'kondums', 'kum', 'kummer', 'kumming', 'kums', 'kunilingus', 'l3i+ch', 'l3itch', 'labia',
             'lmfao', 'lust', 'lusting', 'm0f0', 'm0fo', 'm45terbate', 'ma5terb8', 'ma5terbate', 'masochist',
             'master-bate', 'masterb8', 'masterbat*', 'masterbat3', 'masterbate', 'masterbation', 'masterbations',
             'mo-fo', 'mof0', 'mofo', 'mothafuck', 'mothafucka', 'mothafuckas', 'mothafuckaz', 'mothafucked ',
             'mothafucker', 'mothafuckers', 'mothafuckin', 'mothafucking ', 'mothafuckings', 'mothafucks',
             'mother fucker', 'motherfuck', 'motherfucked', 'motherfuckers', 'motherfuckin', 'motherfucking',
             'motherfuckings', 'motherfuckka', 'motherfucks', 'muff', 'mutha', 'muthafecker', 'muthafuckker', 'muther',
             'mutherfucker', 'n1gga', 'n1gger', 'nazi', 'nigg3r', 'nigg4h', 'niggah', 'niggas', 'niggaz', 'niggers ',
             'nob', 'nob jokey', 'nobhead', 'nobjocky', 'nobjokey', 'numbnuts', 'nutsack', 'orgasim ', 'orgasims ',
             'orgasms ', 'p0rn', 'pawn', 'pecker', 'penisfucker', 'phonesex', 'phuck', 'phuk', 'phuked', 'phuking',
             'phukked', 'phukking', 'phuks', 'phuq', 'pigfucker', 'pimpis', 'piss', 'pissed', 'pisser', 'pissers',
             'pisses ', 'pissflaps', 'pissin ', 'pissoff ', 'poop', 'pornos', 'prick', 'pricks ', 'pron', 'pube',
             'pusse', 'pussi', 'pussys ', 'retard', 'rimjaw', 's hit', 's.o.b.', 'sadist', 'screwing', 'scroat',
             'scrote', 'scrotum', 'sh!+', 'sh!t', 'sh1t', 'shag', 'shagger', 'shaggin', 'shagging', 'shi+', 'shitdick',
             'shite', 'shited', 'shitey', 'shitfuck', 'shitfull', 'shithead', 'shiting', 'shitings', 'shits', 'shitted',
             'shitter', 'shitters ', 'shitting', 'shittings', 'shitty ', 'skank', 'sluts', 'smegma', 'son-of-a-bitch',
             'spac', 'spunk', 's_h_i_t', 't1tt1e5', 't1tties', 'teets', 'teez', 'testical', 'testicle', 'titfuck',
             'titt', 'tittie5', 'tittiefucker', 'tittyfuck', 'tittywank', 'titwank', 'turd', 'tw4t', 'twathead',
             'twatty', 'twunt', 'twunter', 'v14gra', 'v1gra', 'viagra', 'w00se', 'wang', 'wanker', 'wanky', 'whoar',
             'whore', 'willies', 'xrated', 'xxxlesbian sex']

bigram_bad_words = ['sapphic erotica', 'brandi love', '18 year', 'first time', 'massage and', 'porn with',
                    'massage with', 'lesbian girls', 'big cock', 'massage sex', 'porn video', 'lesbian porn',
                    'erotica lesbian', 'lesbian love', 'lesbian babes', 'big ass', 'love porn', 'hard anal',
                    'erotic massage', 'a massage', 'hot teen', 'her ass', 'oil massage', 'happy ending',
                    'lesbian massage', 'milf brandi', 'real homemade', 'lelu love', 'in massage', 'massage rooms',
                    'amateur teen', 'sensual lesbian', 'massage table', 'age teenager', 'teen lesbian', 'ass fucked',
                    'massage room', 'teen girl', 'big boobs', 'on webcam', 'cute teen', 'make love', 'massage babe',
                    'mean lesbian', 'asian massage', 'amateur couple', 'babe gets', 'girl gets', 'body massage',
                    'blonde teen', 'girl with', 'lesbian teens', 'hot milf', 'first porn', 'aaliyah love',
                    'alexis love', 'teen gets', 'hot brunette', 'with busty', 'big tit', 'sucks and', 'sexy lesbian',
                    'mature lady', 'hot blonde', 'on massage', 'russian teen', 'shy love', 'sucking and', 'cum in',
                    'hard cock', 'in lesbian', 'japanese massage', 'soapy massage', 'busty milf', 'massage turns',
                    'slippery massage', 'horny lesbian', 'hot girl', 'massage parlor', 'and facial', 'hot massage',
                    'cock and', 'young girl', 'hot amateur', 'big butt', 'having lesbian', 'brianna love',
                    'during massage', 'after massage', 'slippery nuru', 'cum on', 'brunette teen', 'and cum',
                    'teen angel', 'hot babe', 'loves anal', 'the massage', 'massage from', 'amateur girl', 'horny teen',
                    'teen with', 'hot lesbians', 'first lesbian', 'oily massage', 'blonde babe', 'interracial lesbian',
                    'super hot', 'lesbian teen', 'blonde milf', 'erotic lesbian', 'live webcam', 'hidden cam',
                    'sexy blonde', 'monster cock', 'lesbian anal', 'teen slut', 'euro sex', 'painful anal',
                    'teen couple', 'sensual erotic', 'sexy massage', 'massage therapist', 'homemade sex',
                    'real amateur', 'young teen', 'pussy licking', 'busty lesbian', 'punish sex', 'anal compilation',
                    'sex during', 'massage porn', 'shanie love', 'asian masseuse', 'tight pussy', 'casual teen',
                    'dick in', 'get sex', 'anal fucked', 'her tight', 'her anal', 'sexy babe', 'best anal',
                    'amazing lesbian', 'amateur curvy', 'busty babe', 'huge tits', 'brunette with', 'hairy pussy',
                    'rough sex', 'girl fucked', 'luscious babe']

bad_domains_words = ['viagra', 'cialis', 'porn', 'xxx']


class ProfanityCheck:
    """A class to verify the score of the title of the post based on the bag of words."""

    @classmethod
    def score(cls, text):
        """Calculating the score based on the bad_words and bigram words"""
        text = text.lower()

        # removing the bad words from the sentences to increase the accuracy.

        words_count = [text for text in text.split() if text not in stopwords.words('english')]

        # total words count to calculate the score from

        words_count = len(words_count)

        scoring = 0
        for bad_word in bad_words:
            if text.__contains__(bad_word):
                scoring += 1

        for bad_word in bigram_bad_words:
            if text.__contains__(bad_word):
                scoring += 1
        return scoring / words_count * 100

    @classmethod
    def domain(cls, domain_url):
        """checking the doamin URL, if it is found in the adult URL or contain the bad words.
        @:return True, if the domain has been found, else return false. If false, the domain can be
        added.
        """
        bf = BloomFilter(10000000, 0.01)
        path = os.path.dirname(os.path.abspath(__file__))
        file = open(path + "/data/porn_sites_list.txt", "r+")
        files = file.readlines()
        for item in files:
            bf.add(item.strip())
        file.close()
        result = domain_url in bf
        if result:
            return True
        else:
            for word in bad_domains_words:
                if domain_url.__contains__(word):
                    return True
        return False


class BagOfWords:
    """A class to generate the bag of words from the titles provided."""

    def common(self):
        """
        Finding the most common words from the sentence. This will be used further
        """
        words_list = []
        path = os.path.dirname(os.path.abspath(__file__))
        lines = open(path + "/data/titles.txt", "r").readlines()

        for line in lines:
            words = line.lower().split()

            for word in words:
                if word not in stopwords.words('english'):

                    # added length and domain check.

                    if len(word) >= 3 and not word.__contains__('.'):
                        words_list.append(word)

        for common_words_list in Counter(words_list).most_common():
            if common_words_list[1] > 10:
                if common_words_list[0] not in bad_words:
                    with open(path + "/data/bag_of_words.txt", "a+") as w:
                        w.write(common_words_list[0] + "\n")

    def bigrams(self):
        """
        Generating the list of bigrams from the titles.
        :return: Does not write anything, we are storing the bag of words to the files.
        """
        words_list = []
        path = os.path.dirname(os.path.abspath(__file__))
        lines = open(path + "/data/titles.txt", "r").readlines()

        for line in lines:
            words = line.lower().split()
            bigram = list(nltk.bigrams(words))
            for bg in bigram:
                word = (" ".join(bg))
                if not word in stopwords.words('english'):
                    words_list.append(word)

        for common_words_list in Counter(words_list).most_common():
            if common_words_list[1] > 10:
                if common_words_list[0] not in bad_words:
                    with open(path + "/data/bag_of_words.txt", "a+") as w:
                        w.write(common_words_list[0] + "\n")

    def bigram_to_dict(self):
        """
        Bigram list generator, we can add them directly to the dict after we have the good list.
        """
        words = """sapphic erotica
brandi love
18 year
first time
massage and
porn with
massage with
lesbian girls
big cock
massage sex
porn video
lesbian porn
erotica lesbian
lesbian love
lesbian babes
big ass
love porn
hard anal
erotic massage
a massage
hot teen
her ass
oil massage
happy ending
lesbian massage
milf brandi
real homemade
lelu love
in massage
massage rooms
amateur teen
sensual lesbian
massage table
age teenager
teen lesbian
ass fucked
massage room
teen girl
big boobs
on webcam
cute teen
make love
massage babe
mean lesbian
asian massage
amateur couple
babe gets
girl gets
body massage
blonde teen
girl with
lesbian teens
hot milf
first porn
aaliyah love
alexis love
teen gets
hot brunette
with busty
big tit
sucks and
sexy lesbian
mature lady
hot blonde
on massage
russian teen
shy love
sucking and
cum in
hard cock
in lesbian
japanese massage
soapy massage
busty milf
massage turns
slippery massage
horny lesbian
hot girl
massage parlor
and facial
hot massage
cock and
young girl
hot amateur
big butt
having lesbian
brianna love
during massage
after massage
slippery nuru
cum on
brunette teen
and cum
teen angel
hot babe
loves anal
the massage
massage from
amateur girl
horny teen
teen with
hot lesbians
first lesbian
oily massage
blonde babe
interracial lesbian
super hot
lesbian teen
blonde milf
erotic lesbian
live webcam
hidden cam
sexy blonde
monster cock
lesbian anal
teen slut
euro sex
painful anal
teen couple
sensual erotic
sexy massage
massage therapist
homemade sex
real amateur
young teen
pussy licking
busty lesbian
punish sex
anal compilation
sex during
massage porn
shanie love
asian masseuse
tight pussy
casual teen
dick in
get sex
anal fucked
her tight
her anal
sexy babe
best anal
amazing lesbian
amateur curvy
busty babe
huge tits
brunette with
hairy pussy
rough sex
girl fucked"""
        return words.splitlines()

    def string_to_dict(self):
        """
        Collected the words list comma separted, here we are adding them to the list.
        """
        final_words = []
        items = """4r5e, 5h1t, 5hit, a55, anal, anus, ar5e, arrse, arse, ass, ass-fucker, asses, assfucker, assfukka, asshole, assholes, asswhole, a_s_s, b!tch, b00bs, b17ch, b1tch, ballbag, balls, ballsack, bastard, beastial, beastiality, bellend, bestial, bestiality, bi+ch, biatch, bitch, bitcher, bitchers, bitches, bitchin, bitching, bloody, blow job, blowjob, blowjobs, boiolas, bollock, bollok, boner, boob, boobs, booobs, boooobs, booooobs, booooooobs, breasts, buceta, bugger, bum, bunny fucker, butt, butthole, buttmuch, buttplug, c0ck, c0cksucker, carpet muncher, cawk, chink, cipa, cl1t, clit, clitoris, clits, cnut, cock, cock-sucker, cockface, cockhead, cockmunch, cockmuncher, cocks, cocksuck , cocksucked , cocksucker, cocksucking, cocksucks , cocksuka, cocksukka, cok, cokmuncher, coksucka, coon, cox, crap, cum, cummer, cumming, cums, cumshot, cunilingus, cunillingus, cunnilingus, cunt, cuntlick , cuntlicker , cuntlicking , cunts, cyalis, cyberfuc, cyberfuck , cyberfucked , cyberfucker, cyberfuckers, cyberfucking , d1ck, damn, dick, dickhead, dildo, dildos, dink, dinks, dirsa, dlck, dog-fucker, doggin, dogging, donkeyribber, doosh, duche, dyke, ejaculate, ejaculated, ejaculates , ejaculating , ejaculatings, ejaculation, ejakulate, f u c k, f u c k e r, f4nny, fag, fagging, faggitt, faggot, faggs, fagot, fagots, fags, fanny, fannyflaps, fannyfucker, fanyy, fatass, fcuk, fcuker, fcuking, feck, fecker, felching, fellate, fellatio, fingerfuck , fingerfucked , fingerfucker , fingerfuckers, fingerfucking , fingerfucks , fistfuck, fistfucked , fistfucker , fistfuckers , fistfucking , fistfuckings , fistfucks , flange, fook, fooker, fuck, fucka, fucked, fucker, fuckers, fuckhead, fuckheads, fuckin, fucking, fuckings, fuckingshitmotherfucker, fuckme , fucks, fuckwhit, fuckwit, fudge packer, fudgepacker, fuk, fuker, fukker, fukkin, fuks, fukwhit, fukwit, fux, fux0r, f_u_c_k, gangbang, gangbanged , gangbangs , gaylord, gaysex, goatse, god-dam, god-damned, goddamn, goddamned, hardcoresex , hell, heshe, hoar, hoare, hoer, homo, hore, horniest, horny, hotsex, jack-off , jackoff, jap, jerk-off , jism, jiz , jizm , jizz, kawk, knob, knobead, knobed, knobend, knobhead, knobjocky, knobjokey, kock, kondum, kondums, kum, kummer, kumming, kums, kunilingus, l3i+ch, l3itch, labia, lmfao, lust, lusting, m0f0, m0fo, m45terbate, ma5terb8, ma5terbate, masochist, master-bate, masterb8, masterbat*, masterbat3, masterbate, masterbation, masterbations, masturbate, mo-fo, mof0, mofo, mothafuck, mothafucka, mothafuckas, mothafuckaz, mothafucked , mothafucker, mothafuckers, mothafuckin, mothafucking , mothafuckings, mothafucks, mother fucker, motherfuck, motherfucked, motherfucker, motherfuckers, motherfuckin, motherfucking, motherfuckings, motherfuckka, motherfucks, muff, mutha, muthafecker, muthafuckker, muther, mutherfucker, n1gga, n1gger, nazi, nigg3r, nigg4h, nigga, niggah, niggas, niggaz, nigger, niggers , nob, nob jokey, nobhead, nobjocky, nobjokey, numbnuts, nutsack, orgasim , orgasims , orgasm, orgasms , p0rn, pawn, pecker, penis, penisfucker, phonesex, phuck, phuk, phuked, phuking, phukked, phukking, phuks, phuq, pigfucker, pimpis, piss, pissed, pisser, pissers, pisses , pissflaps, pissin , pissing, pissoff , poop, porn, porno, pornography, pornos, prick, pricks , pron, pube, pusse, pussi, pussies, pussy, pussys , rectum, retard, rimjaw, rimming, s hit, s.o.b., sadist, schlong, screwing, scroat, scrote, scrotum, semen, sex, sh!+, sh!t, sh1t, shag, shagger, shaggin, shagging, shemale, shi+, shit, shitdick, shite, shited, shitey, shitfuck, shitfull, shithead, shiting, shitings, shits, shitted, shitter, shitters , shitting, shittings, shitty , skank, slut, sluts, smegma, smut, snatch, son-of-a-bitch, spac, spunk, s_h_i_t, t1tt1e5, t1tties, teets, teez, testical, testicle, tit, titfuck, tits, titt, tittie5, tittiefucker, titties, tittyfuck, tittywank, titwank, tosser, turd, tw4t, twat, twathead, twatty, twunt, twunter, v14gra, v1gra, vagina, viagra, vulva, w00se, wang, wank, wanker, wanky, whoar, whore, willies, xrated, xxxlesbian sex"""
        for item in (items.split(", ")):
            if not item in bad_words:
                final_words.append(item)
        return final_words
