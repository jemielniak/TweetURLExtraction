from sklearn.feature_extraction.text import TfidfVectorizer
import csv
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
import numpy as np
from random import shuffle

# Imports for decision tree viz
from sklearn.externals.six import StringIO 
from IPython.display import Image
from sklearn.tree import export_graphviz
import pydotplus

bool_array = []

def createCorpus(csvFile):
    corpus_array = []
    
    csv_fp = open(csvFile, "r", encoding="utf8")
    reader = csv.reader(csv_fp)
    rows = [row for row in reader]
    csv_fp.close()
   
    # Shuffle rows to remove bias
    shuffle(rows)
   
    trues = 0
    falses = 0

    for row in rows:
        if len(row[4]) != 0:
            corpus_array.append(row[4])
            if row[1].lower() == "false" or row[2] != "200" or len(row[4]) == 0:
                bool_array.append(0)
                falses = falses + 1
            else:
                bool_array.append(1)
                trues = trues + 1
    print("Number of good links: " + str(trues))
    print("Number of bad links: " + str(falses))
    
    return corpus_array


# Reading data
print("Reading in data")
corpus = createCorpus("../data/url_info.csv")
stop_words = [x.strip() for x in open('../data/stop_words.txt','r').read().split('\n')]

# Creating TFIDF vectors
print("Creating TFIDF vectors")
vectorizer = TfidfVectorizer(stop_words=stop_words)
K = vectorizer.fit_transform(corpus)

# Train vectors
y = np.array(bool_array)[0:2400]
X = K[0:2400]

# Test vectors
y2 = np.array(bool_array)[2400:]
X2 = K[2400:]
	
# Training RandomForestClassifier
print("Training RandomForestClassifier")
clf = RandomForestClassifier(max_depth=10, random_state=0)
clf.fit(X, y)

# Testing RandomForestClassifier
print("Testing RandomForestClassifier")
score_forest = clf.score(X2, y2)

# Training DecisionTreeClassifier
print("Training DecisionTreeClassifier")
cld = DecisionTreeClassifier(random_state = 0, max_depth = 5, min_samples_leaf = 20)
cld.fit(X, y)

# Testing DecisionTreeClassifier
print("Testing DecisionTreeClassifier")
score_decisiontree = cld.score(X2, y2)

# Printing out test results
print("Random Forest accuracy: %s" % score_forest)
print("Decision Tree accuracy: %s" % score_decisiontree)

# Creating decision tree visualization
print("Creating Decision Tree visualization")

vocab = vectorizer.vocabulary_
reverse = {vocab[key] : key for key in vocab}
words = []
for i in range(0, len(reverse)):
    words.append(reverse[i])

dot_data = StringIO()
export_graphviz(cld, out_file=dot_data,
                filled=True, rounded=True,
                special_characters=True,
                class_names = ["Bad link", "Good link"],
                feature_names = words)
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
graph.write_png("../data/viz.png")

txt = ["parkland fla what started out a an ordinary day at a south florida high school ha ended in gunfire and death it happened about 20 mile northwest of fort lauderdale at marjory stoneman douglas high school which is attended by about 3000 student at least 17 people were killed a 19yearold suspected gunman ha been identified a nikolas cruz a former student florida student hid in classroom closet in deadly school shooting a law enforcement source tell cbs news that gunman appears to have pulled the school fire alarm in order to create chaos and then began firing dramatic cellphone video captured the gunfire and the scream of the high school student trapped inside their classroom some hiding in closet a the shooting happened the sight of whats become an alltoofamiliar panic of student fleeing hand raised in single file wa only matched by the image of armed tactical police racing into the building looking for the gunman from the air emergency crew could be seen tending to the wounded and dressing their wound approximately 14 people were transported to area hospital with various degree of injury there are multiple causality there are folk who have lost their life broward county sheriff scott israel said shooting at high school in parkland florida shooting at high school in parkland florida the sheriff say cruz the alleged gunman wa captured off campus he wa seen surrounded by police being placed into custody he wa taken in about an hour after he left douglas after he committed this horrific homicidal act israel said high school freshman bruna aleveda said the gunman wa just outside their door i dont know how we are alive she said for like 30 minute we were like praying and cry and then the police came and we just got out when the lockdown wa over distraught parent raced to the scene they were even more emotional teenager relieved to be outside it a horrific situation it a horrible day for u school superintendent robert runcie said",
       "the umpqua community college shooting occurred on october 1 2015 at the ucc campus near roseburg oregon united state chris harpermercer a 26yearold enrolled at the school fatally shot an assistant professor and eight student in a classroom eight others were injured roseburg police detective responding to the incident engaged harpermercer in a brief shootout after being wounded he killed himself by shooting himself in the head the mass shooting wa the deadliest in oregon modern history a content 1\tshooting 11\taftermath 2\tvictims 21\tfatalities 22\tinjured 3\tperpetrator 4\treactions 5\tsee also 6\tnotes 7\treferences shooting at 1038 am pdt the first 911 call wa made from snyder hall on the school campus reporting gunfire student reported that the shooting began in classroom 15 where english and writing class are conducted 4 5 harpermercer who wa a student in the writing class entered the classroom and fired a warning shot 6 some witness said he then forced fellow student to the center of the classroom before he opened fire on the other student he deliberately spared one student life so that student could deliver a package from him to police he forced this student to sit at the back of the classroom and watch a he continued shooting with two handgun glock 19 and taurus pt247 7 8 9 harpermercer first shot the assistant english professor at pointblank range he allegedly asked two student for their religion shooting them after they gave him a response 6 10 other witness said he asked if student were christian telling those who replied in the affirmative that they would go to heaven a he shot them although one victim wa agnostic 11 and another wa pagan 12 some student were shot multiple time 6 13 one woman wa struck several time in the stomach while trying to close a classroom door 14 one witness said he made a woman beg for her life before shooting her shot another woman when she tried to reason with him 15 and shot a third woman in the leg after she tried to defend herself with a desk 10 one victim sarena dawn moore wa killed while trying to climb back into a wheelchair at his order 6 16 two plainclothes detective from the roseburg police department were the first to respond to the scene they arrived at the hallway of snyder hall at 1044 six minute after the first 911 call wa received two minute later harpermercer reloaded his handgun and leaned out of the classroom firing several shot at the officer they fired three shot in return hitting him once in the right side 17 after two more minute of shooting at the officer the wounded harpermercer retreated into the classroom and killed himself with a single shot to his head 6 8 18 19 none of the officer were injured 2 20 21 aftermath following the shooting bureau of alcohol tobacco firearm and explosive atf agent launched a campuswide search for explosive six firearm were recovered from the crime scene 22 five handgun and one long gun none were owned by his mother 23 24 25 the long gun a 556x45mm delton dti15 semiautomatic rifle wa not used during the incident 26 harpermercer also had a flak jacket and enough ammunition for a prolonged gunfight 27 28 police said they found eight other firearm at his apartment and that all of the weapon were purchased legally by him or member of his family 19 29 victim fatality harpermercer killed eight student and a teacher lawrence levine eight died at the scene and the ninth died at mercy medical center the dead were 30 31 lucero alcaraz aged 19 treven taylor anspach 20 rebecka ann carnes 18 32 quinn glen cooper 18 kim saltmarsh dietz 59 lucas eibel 18 jason dale johnson 33 lawrence levine 67 sarena dawn moore 44 injured eight other student were injured 33 34 some with multiple gunshot wound 30 35 among the wounded wa chris mintz a u army veteran who wa studying fitness training at the college 36 who responded when he heard scream coming from an adjacent classroom he blocked the connected door with his body to allow his class to escape he next left the building to alert student in the library to evacuate returning to the shooting scene he advised a wounded student to stay down and be quiet at that point harpermercer leaned out from the classroom into the hallway and shot mintz five time a he wa first standing then falling to the floor because he said mintz had called police mintz pleaded that he not be killed on his son birthday and said an apparently emotionless harpermercer withdrew back into the classroom 37 at a press conference held on october 3 douglas county sheriff john hanlin thanked mintz for his action 38 to help pay for his medical bill mintzs family set up a gofundme account by the end of that day it had already received more than us650000 in donation 39 mintz wa released from a hospital on october 7 40 on october 13 a 16yearold girl who wa critically wounded in the shooting wa released from a hospital 41 perpetrator christopher harpermercer born\tjuly 26 1989 los angeles county california died\toctober 1 2015 aged 26 roseburg oregon cause of death\tsuicide nationality\tamerican alma mater\tel camino college occupation\tstudent parents\tian mercer father laurel harper mother christopher sean chris harpermercer 30 july 26 1989 october 1 2015 wa enrolled in the introductory composition class where he shot his victim 30 42 he wa born in los angeles county california to ian mercer and laurel margaret harper and lived with his mother during the separation and divorce of his parent who agreed to shared legal custody harpermercer continued to live with his mother and remained with her when she moved to oregon for work 43 his father had not seen him for about two year following his son move out of state 44 45 46 harpermercer joined the u army in 2008 but wa discharged after five week for his failure to meet the minimum administrative standard of basic training at fort jackson south carolina 30 47 official linked to the investigation said that he wa discharged a the result of a suicide attempt but army official did not comment on this 48 in 2009 he graduated from switzer learning center a school for teenager with learning disability or emotional issue 19 49 laurel harper wa reportedly protective of him 50 and tried to shield him from various perceived annoyance some of them minor in their neighborhood in torrance california 47 from early 2010 to early 2012 harpermercer attended el camino college in torrance 51 harpermercer maintained several internet account including one in which he described himself a mixed race 52 53 b medium report said he had an email address linked to an account on a bittorrent website the last upload on the account three day before the umpqua shooting wa a documentary on the sandy hook elementary school shooting 56 57 according to the los angeles time unnamed law enforcement source described him a a hatefilled man with antireligious and white supremacist leaning and with longterm mentalhealth issue 58 his mother laurel harper had previously written anonymously in an online forum that both she and her son had asperger syndrome 59 60 he and his mother moved to winchester oregon in 2013 after she received a job there 43 47 there were fourteen legally purchased weapon kept in the apartment and harpermercers mother wrote online that she always kept full magazine in glock pistol and an ar15 rifle inside 61 the two often spent time together at shooting range but harpermercer wa otherwise extremely isolated 62 harpermercer had been placed on academic probation at umpqua community college for falling below a c average a letter dated september 1 warned him that he could be suspended if he did not raise his grade a ucc tuition bill due on october 6 noted that harpermercer owed 2021 51 on the day of the shooting harpermercer gave a survivor numerous writing showing he had studied mass killing including the 2014 killing spree at isla vista california 63 these expressed his sexual frustration a a virgin animosity toward black men and a lack of fulfillment in his isolated life 64 65 66 in them he said other people think im crazy but im not im the sane one 67 and that he would be welcomed in hell and embraced by the devil 68 he also reportedly admired the perpetrator of the wdbj shooting for the fame received and wrote that a man who wa known by no one is now known by everyone his face splashed across every screen his name across the lip of every person on the planet all in the course of one day 69 70 71 reaction filethe president delivers a statement on the shooting in oregonwebm video of president obama delivering a statement on the shooting 1244 c oregon governor kate brown said she wa heartbroken by the event and that she would immediately travel to roseburg the american association of community college and the association of community college trustee issued a joint statement calling the shooting a tragedy and expressing their commitment to oncampus safety 72 sheriff john hanlin of douglas county said he would not name the shooter i will not give him credit for this horrific act of cowardice medium will get the name confirmed in time but you will never hear u use it 73 d u president barack obama said that thought and prayer do not capture the heartache and grief and anger that we should feel and it doe nothing to prevent this carnage from being inflicted some place else in america next week or a couple month from now c he ordered the u flag to be flown at half staff in memory of the victim the day after the shooting on october 5 the white house announced that obama would continue to take more executive action on the subject of gun control 76 obama wa met at roseburg regional airport by around 200 protester rallying behind a security fence some with holstered weapon who also showed support for sheriff hanlin who had been highly visible during press conference about the shooting after 20 child and six school staff were shot and killed in 2012 at sandy hook elementary school hanlin had sent a letter to vice president joe biden saying he would not enforce any new gun legislation he deemed to be unconstitutional 77 although harpermercer had suffered from substantial mental illness he had never been involuntarily committed which under federal and state law prohibits a person from purchasing a gun harpermercer wa therefore able to pas a background check and bought a 380 semiautomatic handgun 78 an oregon law passed in 2017 which went into effect in 2018 allows law enforcement or family member to file a petition in state court for an extreme risk protection order such an order if granted temporarily block an individual from purchasing or possessing deadly weapon if the individual is determined to present an imminent threat to themselves or others 78 had the law been in effect earlier it is possible that harpermercer could have been prevented from purchasing his weapon 78",
       "roseburg ore a 26yearold man opened fire on a community college campus here in a rampage that left 10 people dead and seven wounded and turned this rural stretch of southern oregon into the latest american locale ravaged by a mass shooting student described scene of carnage concentrated in a public speaking class that wa underway in a college humanity building and people fleeing in panic from classroom a they heard shot nearby the college umpqua community college went into lockdown and the gunman died in an exchange of gunfire with police officer who responded law enforcement official said with anxious parent waiting at a fairground near the campus and the police going from classroom to classroom the authority report of the death toll varied throughout the day at a 5 pm news conference john hanlin the sheriff of douglas county said that he believed there were 10 dead calling the toll the best most accurate information we have at this time he declined to say whether the gunman wa included in the death toll photo patient were taken to mercy medical center in roseburg ore credit aaron yostroseburg newsreview via associated press law enforcement official identified the gunman thursday night a chris harper mercer and said he had three weapon at least one of them a long gun and the other one handgun it wa not clear whether he fired them all the official said the man lived in the roseburg area they said one witness had told them that mr mercer had asked about people religion before he began firing he appears to be an angry young man who wa very filled with hate one law enforcement official said investigator are poring over what one official described a hateful writing by mr mercer the fbi ha dispatched dozen of agent to assist in the investigation continue reading the main story related coverage oregon killer described a man of few word except on topic of gun oct 2 2015 obama condemns routine of mass shooting say u ha become numb oct 1 2015 retro report when columbine is invoked fear tend to overshadow fact sept 27 2015 recent comment peter rennie october 5 2015 whilst our heart go to everyone affected by this tragedy our head need to see a bigger picture from the perspective of someone who ha sam hill october 5 2015 step back and calm down how wa this nut case stopped he wa stopped by men with gun yes gun they were cop but they didnt have to mo october 5 2015 while i am for sane gun control law here i wonder how many of the people posting outraged sentiment about this latest mass murder would see all comment sheriff hanlin said at a news conference that he would not speak the gunman name let me be very clear i will not name the shooter he said i will not give him the credit he probably sought prior to this horrific and cowardly act he also encouraged reporter not to glorify and create sensationalism for him he in no way deserves it the massacre added the community college to a string of school that have been left grieving after mass shooting a list that run from columbine high school in 1999 to virginia tech in 2007 to sandy hook elementary school in newtown conn where 20 child were killed in 2012 photo family and friend were reunited at a nearby fairground after a gunman opened fire at umpqua community college in roseburg ore credit ryan kangassociated press president obama in an impassioned appearance at the white house said that grief wa not enough and he implored american whether they are democrat or republican or independent to consider their representative stance on gun control when they voted and to decide whether this cause of continuing death for innocent people should be a relevant factor state and local official all expressed shock gov kate brown said at a news conference that she felt profound dismay and heartbreak the first report of shot came at 1038 am on what wa the fourth day of the new session student said they took place in classroom 15 in a building called snyder that house many english and writing class cassandra welding a 20yearold junior wa in classroom 16 next to the shooting and heard several loud burst like balloon popping there were about 20 people in the classroom a middleaged woman behind her rose to shut the classroom door and wa struck in the stomach by several bullet he wa just out there hanging outside the door m welding said of the gunman and she slumped over and i knew something wasnt right and theyre like she got shot she got shot and everyone is panicking continue reading the main story continue reading the main story oregon roseburg north umpqua river teacher office umpqua community college classroom snyder hall the shooting occurred in this section of the building snyder hall oregon roseburg umpqua community college snyder hall teacher office classroom snyder hall the shooting occurred in this section of the building source sarah cobb a student at the university and other witness account by the new york time aerial image via google earth a friend of the injured woman dragged her into the room and began delivering cpr m welding said someone clicked the door shut and the student huddled in the corner blocking themselves with desk and backpack i heard more shooting m welding said it wa horrific my whole body wa shaking a chill wa going down my spine we called 911 she added i wa on the phone with my mom pretty much the entire time i knew this could have been the last time i talked to her brady winder 23 who moved to roseburg only three week ago wa in a writing class we heard one shot mr winder said it sounded like someone dropped something heavy on the floor and everybody kind of startled there a door connecting our classroom to that classroom and my teacher wa going to knock on the door but she called out is everybody ok and then we heard a bunch more shot we all froze for about half a second everybodys head turned and looked at each other trying to just grasp what wa happening and someone said those are gunshot we heard people screaming next door and then everybody took off people were hopping over desk knocking thing over kortney moore 18 from rogue river told the roseburg newspaper the newsreview that the gunman had asked people to stand up and state their religion and then started firing she said she saw her teacher shot in the head adding that she herself wa on the floor with people who had been shot federal law enforcement official said they were examining an online conversation on 4chan an anonymous message board a well a other social medium trying to determine whether any of it wa linked to the gunman in that conversation one writer said dont go to school tomorrow if you are in the northwest news clip by reuters 0034 dispatcher alert police of shooting video dispatcher alert police of shooting on thursday afternoon police officer secured the scene of a mass shooting at umpqua community college in roseburg ore by reuters on publish date october 1 2015 photo by mike sullivanroseburg newsreview via associated press watch in time video embed sharetweet roseburg about 180 mile south of portland with a population of 22000 is a part of the pacific northwest that in many way ha been left behind a the region ha moved on toward an economy of technology and high wage once a major center for wood milling it ha struggled in recent decade a the timber harvest in the national forest that hug the community have declined wine grape cultivation ha helped some but poverty and unemployment rate are high in august according to the most recent government figure douglas county had an unemployment rate of 81 percent tied for the secondhighest in the state about 20 percent of resident in the city and county live below the federal poverty line the college with about 3000 student reflects that struggle with many of it student coming back to school to gain skill for a career change the average student is 37 and popular course of study include winemaking nursing welding and auto mechanic it a community college so a lot of our friend and family attend this college sheriff hanlin said joe olson who retired a president of umpqua community college at the end of june said that within the past several month the college had discussed hiring an armed security guard but had ultimately decided against it we talked about that over the last year because we were concerned about safety on campus he said the campus wa split 5050 we thought we were a very safe campus and having armed security officer on campus might change the culture photo personnel from several law enforcement agency converged on the campus we all froze for about half a second when the shot broke out one student said credit michael sullivanthe newsreview via associated press he added though that he did not believe a security guard could prevent a gunman determined to kill if you want to come on the campus and you want to shoot five people you are going to do that before our security would arrive he said oregon is one of seven state with provision either from state legislation or court ruling that allow the carrying of concealed weapon on public postsecondary campus according to the national conference of state legislature the other state are colorado idaho kansa mississippi utah and wisconsin numerous law enforcement agency responded to thursday shooting corey ray a spokesman for the bureau of alcohol tobacco firearm and explosive said the agency wa sending team including canine team from seattle portland and eugene ore they will join a team already on the ground that is helping search for firearm casing and other ammunition the apartment complex where the gunman had lived wa roped off with police tape and under guard by deputy last night bronte hart 21 said she lived beneath mr mercer who she said would frequently shout at her for smoking on her balcony news clip by the associated press 223 obama on oregon college shooting video obama on oregon college shooting the president delivered remark from the white house after a gunman opened fire at umpqua community college in roseburg ore by the associated press on publish date october 1 2015 photo by zach gibsonthe new york time watch in time video embed sharetweet he yelled at u me and my husband said m hart who life in the complex with her husband and father he wa not a friendly type of guy he did not want anything to do with anyone m hart and her father eli loomas said the authority had shown up at the complex in the morning and begun asking question about mr mercer eight mile south of the college at a cordonedoff hall on the douglas county fairground family member spent agonizing hour waiting to hear of possible victim a student were evacuated there the police searched everybody mr winder one of the student said searching their jacket and bag for weapon before putting them on bus among those waiting were jessica chandler whose daughter 18yearold rebecka carnes started class at umpqua on monday her daughter an aspiring dental hygienist had not responded to dozen of call a friend told m chandler that the teenager had been taken to a hospital but the police and hospital official would not confirm it recurring sorrow president obamas remark after gun violence she always ha her cellphone and is always in contact m chandler said smoking a cigarette outside the family waiting area i want to know where my kid is many student at the school talked about tiny detail that stuck with them a they ran and how they had tried to piece together information a they hid and hoped to stay alive joanah fallin wa headed toward the campus around 1030 am when he saw a police car go by at what he estimated wa 120 mile an hour ive never seen any car go that fast he said by the time he reached campus it wa already in mayhem lot of people were cry he said there wa a woman with a child it wa just unbelievable luke rogers another student wa in the building next door to the shooting he said he and his classmate were locked in the building from 1030 am until noon with the only access to information about the shooting coming from text from friend and family when we exited the building the officer made u put our hand above our head and leave in a singlefile line he said a we passed snyder hall we saw the door open and on the ground there were drop of blood",
       ]

print(cld.predict_proba(vectorizer.transform(txt)))
print(clf.predict_proba(vectorizer.transform(txt)))