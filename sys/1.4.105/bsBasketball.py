import bs
import random

def bsGetAPIVersion():
    # see bombsquadgame.com/apichanges
    return 4

def bsGetGames():
    return [BasketballTeamGame]

class BasketballTeamGame(bs.TeamGameActivity):

    @classmethod
    def getName(cls):
        return 'Basketball'

    @classmethod
    def supportsSessionType(cls,sessionType):
        return True if issubclass(sessionType,bs.TeamsSession) else False
    
    @classmethod
    def getDescription(cls,sessionType):
        return 'Throw the ball to the enemy goalie.'

    @classmethod
    def getSupportedMaps(cls,sessionType):
        return bs.getMapsSupportingPlayType('basketball')

    @classmethod
    def getSettings(cls,sessionType):
        return [("Score to Win",{'minValue':1,'default':3,'increment':1}),
                ("Time Limit",{'choices':[('None',0),('1 Minute',60),
                                        ('2 Minutes',120),('5 Minutes',300),
                                        ('10 Minutes',600),('20 Minutes',1200)],'default':0}),
                ("Respawn Times",{'choices':[('Shorter',0.25),('Short',0.5),('Normal',1.0),('Long',2.0),('Longer',4.0)],'default':1.0}),
                ]

    def __init__(self,settings):
        bs.TeamGameActivity.__init__(self,settings)
        self._scoreBoard = bs.ScoreBoard()

        # load some media we need
        self._cheerSound = bs.getSound("cheer")
        self._chantSound = bs.getSound("crowdChant")
        self._scoreSound = bs.getSound("score")
        self._swipSound = bs.getSound("swip")
        self._whistleSound = bs.getSound("refWhistle")

        self.scoreRegionMaterial = bs.Material()
        self.scoreRegionMaterial.addActions(
            conditions=("theyHaveMaterial",bs.Bomb.getFactory().basketballSoundMaterial),
            actions=(("modifyPartCollision","collide",True),
                     ("modifyPartCollision","physical",False),
                     ("call","atConnect",self._handleScore)))

    def getInstanceDescription(self):
        tds = self.settings['Score to Win']
        if tds > 1: return ('Score ${ARG1} goals.',tds)
        else: return ('Score a goal.')

    def getInstanceScoreBoardDescription(self):
        tds = self.settings['Score to Win']
        if tds > 1: return ('score ${ARG1} goals',tds)
        else: return ('score a goal')

    def onTransitionIn(self):
        bs.TeamGameActivity.onTransitionIn(self, music='Football')

    def onBegin(self):
        bs.TeamGameActivity.onBegin(self)

        self.setupStandardTimeLimit(self.settings['Time Limit'])
        self.setupStandardPowerupDrops()

        self._flagSpawnPos = self.getMap().getFlagPosition(None)
        self._spawnFlag()

        # set up the two score regions
        self._scoreRegions = []

        defs = self.getMap().defs
        self._scoreRegions.append(bs.NodeActor(bs.newNode('region',
                                                          attrs={'position':defs.boxes['goal1'][0:3],
                                                                 'scale':defs.boxes['goal1'][6:9],
                                                                 'type': 'box',
                                                                 'materials':(self.scoreRegionMaterial,)})))
        
        self._scoreRegions.append(bs.NodeActor(bs.newNode('region',
                                                          attrs={'position':defs.boxes['goal2'][0:3],
                                                                 'scale':defs.boxes['goal2'][6:9],
                                                                 'type': 'box',
                                                                 'materials':(self.scoreRegionMaterial,)})))
        self._updateScoreBoard()

        bs.playSound(self._chantSound)

    def onTeamJoin(self,team):
        team.gameData['score'] = 0
        self._updateScoreBoard()

    def _killFlag(self):
        self._flag = None

    def _handleScore(self):
        """ a point has been scored """

        # our flag might stick around for a second or two
        # make sure it doesn't score again
        if self._flag.scored: return

        region = bs.getCollisionInfo("sourceNode")
        for i in range(len(self._scoreRegions)):
            if region == self._scoreRegions[i].node:
                break;

        for team in self.teams:
            if team.getID() == i:
                team.gameData['score'] += 1

                # tell all players to celebrate
                for player in team.players:
                    try: player.actor.node.handleMessage('celebrate',2000)
                    except Exception: pass

                # if someone on this team was last to touch it, give them points
                if (self._flag.lastHoldingPlayer is not None and self._flag.lastHoldingPlayer.exists()
                    and team == self._flag.lastHoldingPlayer.getTeam()):
                    self.scoreSet.playerScored(self._flag.lastHoldingPlayer,50,bigMessage=True)

                # end game if we won
                if team.gameData['score'] >= self.settings['Score to Win']:
                    self.endGame()

        bs.playSound(self._scoreSound)
        bs.playSound(self._cheerSound)

        self._flag.scored = True

        # kill the flag (it'll respawn shortly)
        bs.gameTimer(1000,self._killFlag)
        bs.gameTimer(3000,self._spawnFlag)

        light = bs.newNode('light',
                           attrs={'position': bs.getCollisionInfo('position'),
                                  'heightAttenuated':False,
                                  'color': (1,0,0)})
        bs.animate(light,'intensity',{0:0,500:1,1000:0},loop=True)
        bs.gameTimer(1000,light.delete)

        self.cameraFlash(duration=10)
        self._updateScoreBoard()

    def endGame(self):
        results = bs.TeamGameResults()
        for t in self.teams: results.setTeamScore(t,t.gameData['score'])
        self.end(results=results,announceDelay=800)

    def _updateScoreBoard(self):
        winScore = self.settings['Score to Win']
        for team in self.teams:
            self._scoreBoard.setTeamValue(team,team.gameData['score'],winScore)

    def handleMessage(self,m):

        if isinstance(m,bs.FlagPickedUpMessage):
            try:
                player = m.node.getDelegate().getPlayer()
                if player.exists(): m.flag.lastHoldingPlayer = player
            except Exception:
                bs.printException('exception in Football FlagPickedUpMessage; this shoudln\'t happen')
            m.flag.heldCount += 1

        elif isinstance(m,bs.FlagDroppedMessage):
            m.flag.heldCount -= 1

        # respawn dead players if they're still in the game
        elif isinstance(m,bs.PlayerSpazDeathMessage):
            bs.TeamGameActivity.handleMessage(self,m) # augment standard behavior
            self.respawnPlayer(m.spaz.getPlayer())

        # respawn dead flags
        elif isinstance(m,bs.FlagDeathMessage):
            if not self.hasEnded():
                self._flagRespawnTimer = bs.Timer(3000,self._spawnFlag)
                self._flagRespawnLight = bs.NodeActor(bs.newNode('light',
                                                                 attrs={'position': self._flagSpawnPos,
                                                                        'heightAttenuated':False,
                                                                        'radius':0.15,
                                                                        'color': (1.0,1.0,0.3)}))
                bs.animate(self._flagRespawnLight.node,"intensity",{0:0,250:0.15,500:0},loop=True)
                bs.gameTimer(3000,self._flagRespawnLight.node.delete)

        else:
            bs.TeamGameActivity.handleMessage(self,m) # augment standard behavior

    def _flashFlagSpawn(self):
        light = bs.newNode('light',
                           attrs={'position': self._flagSpawnPos,
                                  'heightAttenuated': False,
                                  'color': (1,1,0)})
        bs.animate(light,'intensity',{0:0,250:0.25,500:0},loop=True)
        bs.gameTimer(1000,light.delete)

    def _spawnFlag(self):
        bs.playSound(self._swipSound)
        bs.playSound(self._whistleSound)
        self._flashFlagSpawn()
        self._flag = bs.Bomb(position=self._flagSpawnPos,
                             bombType='basketball')
        self._flag.scored = False
        self._flag.heldCount = 0
        self._flag.lastHoldingPlayer = None
        self._flag.light = bs.newNode("light",
                                      owner=self._flag.node,
                                      attrs={"intensity":0.25,
                                             "heightAttenuated":False,
                                             "radius":0.2,
                                             "color": (0.9,0.7,0.0)})
        self._flag.node.connectAttr('position',self._flag.light,'position')