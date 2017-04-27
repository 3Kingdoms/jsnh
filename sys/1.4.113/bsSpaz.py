import bs
import bsUtils
import random
import weakref

# jasonhu5
import math
import os
# import inspect

# list of defined spazzes
appearances = {}

def getAppearances(includeLocked=False):
    import bsInternal
    import bsAchievement
    disallowed = []
    if not includeLocked:
        # hmm yeah this'll be tough to hack...
        if not bsInternal._getPurchased('characters.santa'): disallowed.append('Santa Claus')
        if not bsInternal._getPurchased('characters.frosty'): disallowed.append('Frosty')
        if not bsInternal._getPurchased('characters.bones'): disallowed.append('Bones')
        if not bsInternal._getPurchased('characters.bernard'): disallowed.append('Bernard')
        if not bsInternal._getPurchased('characters.pixie'): disallowed.append('Pixel')
        if not bsInternal._getPurchased('characters.pascal'): disallowed.append('Pascal')
        if not bsInternal._getPurchased('characters.actionhero'): disallowed.append('Todd McBurton')
        if not bsInternal._getPurchased('characters.taobaomascot'): disallowed.append('Taobao Mascot')
        if not bsInternal._getPurchased('characters.agent'): disallowed.append('Agent Johnson')
        if not bsInternal._getPurchased('characters.jumpsuit'): disallowed.append('Lee')
        if not bsInternal._getPurchased('characters.assassin'): disallowed.append('Zola')
        if not bsInternal._getPurchased('characters.cowboy'): disallowed.append('Butch')
        if not bsInternal._getPurchased('characters.witch'): disallowed.append('Witch')
        if not bsInternal._getPurchased('characters.warrior'): disallowed.append('Warrior')
        if not bsInternal._getPurchased('characters.superhero'): disallowed.append('Middle-Man')
        if not bsInternal._getPurchased('characters.alien'): disallowed.append('Alien')
        if not bsInternal._getPurchased('characters.oldlady'): disallowed.append('OldLady')
        if not bsInternal._getPurchased('characters.gladiator'): disallowed.append('Gladiator')
        if not bsInternal._getPurchased('characters.wrestler'): disallowed.append('Wrestler')
        if not bsInternal._getPurchased('characters.operasinger'): disallowed.append('Gretel')
        if not bsInternal._getPurchased('characters.pixie'): disallowed.append('Pixie')
        if not bsInternal._getPurchased('characters.robot'): disallowed.append('Robot')
        if not bsInternal._getPurchased('characters.cyborg'): disallowed.append('B-9000')
        if not bsInternal._getPurchased('characters.bunny'): disallowed.append('Easter Bunny')
        if not bsInternal._getPurchased('characters.kronk'): disallowed.append('Kronk')
        if not bsInternal._getPurchased('characters.zoe'): disallowed.append('Zoe')
        if not bsInternal._getPurchased('characters.jackmorgan'): disallowed.append('Jack Morgan')
        if not bsInternal._getPurchased('characters.mel'): disallowed.append('Mel')
        if not bsInternal._getPurchased('characters.snakeshadow'): disallowed.append('Snake Shadow')
        
        # Custom characters that can only be obtained with achievements
        if not bsAchievement.getAchievement('Make It Through').isComplete(): disallowed.append('Mictlan')
        if not bsAchievement.getAchievement('Onslaught God').isComplete(): disallowed.append('Zill')
        if not bsAchievement.getAchievement('The Full Run').isComplete(): disallowed.append('Looie')
        if not bsAchievement.getAchievement('Half-Marathon').isComplete(): disallowed.append('Spy')
        if not bsAchievement.getAchievement('Last Stand God').isComplete(): disallowed.append('Juice-Boy')
        
        # Custom characters that can be obtained from the store
        if not bsInternal._getPurchased('characters.wizard_mr'): disallowed.append('Grumbledorf')
        if not bsInternal._getPurchased('characters.cow_mr'): disallowed.append('Milk')
        
        # AVGN swears. ALOT! What If you have dem kids to play this crap? No problemo!
        if bsInternal._getSetting('Kid Friendly Mode'): disallowed.append('AVGN')
    return [s for s in appearances.keys() if s not in disallowed]

gPowerupWearOffTime = 20000
gPowerfulPowerupWearOffTime = 15000

gBasePunchPowerScale = 1.2
gBasePunchCooldown = 500


gLameBotColor = (1.2,0.9,0.2)
gLameBotHighlight = (1.0,0.5,0.6)

gDefaultBotColor = (0.6,0.6,0.6)
gDefaultBotHighlight = (0.1,0.3,0.1)

gProBotColor = (1.0,0.2,0.1)
gProBotHighlight = (0.6,0.1,0.05)

# jasonhu5
gMoveLeftRight = 0.0
gMoveUpDown = 0.0
# 

class _PickupMessage(object):
    'We wanna pick something up'
    pass

class _PunchHitMessage(object):
    'Message saying an object was hit'
    pass

class _CurseExplodeMessage(object):
    'We are cursed and should blow up now.'
    pass

class _BombDiedMessage(object):
    "A bomb has died and thus can be recycled"
    pass

class Appearance(object):
    """Create and fill out one of these suckers to define a spaz appearance"""
    def __init__(self,name):

        self.name = name

        if appearances.has_key(self.name):
            raise Exception("spaz appearance name \"" + self.name + "\" already exists.")

        appearances[self.name] = self
        self.colorTexture = ""
        self.headModel = ""
        self.torsoModel = ""
        self.pelvisModel = ""
        self.upperArmModel = ""
        self.foreArmModel = ""
        self.handModel = ""
        self.upperLegModel = ""
        self.lowerLegModel = ""
        self.toesModel = ""
        self.jumpSounds = []
        self.attackSounds = []
        self.impactSounds = []
        self.deathSounds = []
        self.pickupSounds = []
        self.fallSounds = []
        self.style = 'spaz'
        self.defaultColor = None
        self.defaultHighlight = None

class SpazFactory(object):
    """
    Category: Game Flow Classes

    Wraps up media and other resources used by bs.Spaz instances.
    Generally one of these is created per bs.Activity and shared
    between all spaz instances.  Use bs.Spaz.getFactory() to return
    the shared factory for the current activity.

    Attributes:

       impactSoundsMedium
          A tuple of bs.Sounds for when a bs.Spaz hits something kinda hard.

       impactSoundsHard
          A tuple of bs.Sounds for when a bs.Spaz hits something really hard.

       impactSoundsHarder
          A tuple of bs.Sounds for when a bs.Spaz hits something really really hard.

       singlePlayerDeathSound
          The sound that plays for an 'importan' spaz death such as in co-op games.

       punchSound
          A standard punch bs.Sound.
       
       punchSoundsStrong
          A tuple of stronger sounding punch bs.Sounds.

       punchSoundStronger
          A really really strong sounding punch bs.Sound.

       swishSound
          A punch swish bs.Sound.

       blockSound
          A bs.Sound for when an attack is blocked by invincibility.

       shatterSound
          A bs.Sound for when a frozen bs.Spaz shatters.

       splatterSound
          A bs.Sound for when a bs.Spaz blows up via curse.

       spazMaterial
          A bs.Material applied to all of parts of a bs.Spaz.

       rollerMaterial
          A bs.Material applied to the invisible roller ball body that a bs.Spaz uses for locomotion.
    
       punchMaterial
          A bs.Material applied to the 'fist' of a bs.Spaz.

       pickupMaterial
          A bs.Material applied to the 'grabber' body of a bs.Spaz.

       curseMaterial
          A bs.Material applied to a cursed bs.Spaz that triggers an explosion.
    """

    def _preload(self,character):
        """
        Preload media that will be needed for a given character.
        """
        self._getMedia(character)

    def __init__(self):
        """
        Instantiate a factory object.
        """

        # Flesh characters
        self.impactSoundsMedium = (bs.getSound('impactMedium'),
                                bs.getSound('impactMedium2'),
								bs.getSound('impactMedium3'),
								bs.getSound('impactMedium4'),
								bs.getSound('impactMedium5'),
								bs.getSound('impactMedium6'),
								bs.getSound('impactMedium7'))
        self.impactSoundsHard = (bs.getSound('impactHard'),
                                bs.getSound('impactHard2'),
                                bs.getSound('impactHard3'),
								bs.getSound('impactHard4'),
								bs.getSound('impactHard5'),
								bs.getSound('impactHard6'))
        self.impactSoundsHarder = (bs.getSound('impactGiant'),
                                   bs.getSound('impactGiant2'),
								   bs.getSound('impactGiant3'),
								   bs.getSound('impactGiant4'),
								   bs.getSound('impactGiant5'),
								   bs.getSound('impactGiant6'))
        # Metal characters (mainly robots)
        self.impactMetalSoundsMedium = (bs.getSound('impactMediumMetal1'),
                                bs.getSound('impactMediumMetal2'))
        self.impactMetalSoundsHard = (bs.getSound('impactHardMetal1'),
                                bs.getSound('impactHardMetal2'))
        self.impactMetalSoundsHarder = (bs.getSound('impactGiantMetal1'),
                                bs.getSound('impactGiantMetal2'))
        # Cardboard characters (for example Juicebox)
        self.impactCardboardSoundsMedium = (bs.getSound('impactMediumCardboard1'),
                                bs.getSound('impactMediumCardboard2'))
        self.impactCardboardSoundsHard = (bs.getSound('impactHardCardboard1'),
                                bs.getSound('impactHardCardboard2'))
        self.impactCardboardSoundsHarder = (bs.getSound('impactGiantCardboard1'),
                                bs.getSound('impactGiantCardboard2'))
        
        self.singlePlayerDeathSound = bs.getSound('playerDeath')
        
        self.punchSound = bs.getSound('punch01')
        self.punchWeakSound = bs.getSound('punchWeak01')
        self.punchSoundsStrong = (bs.getSound('punchStrong01'),
                                  bs.getSound('punchStrong02'))
        self.punchSoundStronger = bs.getSound('superPunch')
        # The CRIT! sound effect
        self.powerPunchSounds = (bs.getSound('owThatHurts1'),
                                bs.getSound('owThatHurts2'))
        self.homeRunSound = bs.getSound('homeRun')
        self.swishSounds = (bs.getSound('punchSwish1'),
                          bs.getSound('punchSwish2'))

        # jasonhu5
        self.hissSound = bs.getSound('activateBeep')
        # 
        
        self.blockSound = bs.getSound('block')
        self.shatterSound = bs.getSound('shatter')
        self.splatterSound = bs.getSound('splatter')
        
        # Speed Up and Down sounds for the Speed Boots powerup
        self.speedUpSound = bs.getSound('speedUp')
        self.speedDownSound = bs.getSound('speedDown')
        
        #Curse Sounds
        self.curseSound = bs.getSound('curse')
        self.curseOffensiveSound = bs.getSound('curseOffensive')
        
        self.spazMaterial = bs.Material()
        self.rollerMaterial = bs.Material()
        self.punchMaterial = bs.Material()
        self.pickupMaterial = bs.Material()
        self.curseMaterial = bs.Material()

        footingMaterial = bs.getSharedObject('footingMaterial')
        objectMaterial = bs.getSharedObject('objectMaterial')
        playerMaterial = bs.getSharedObject('playerMaterial')
        regionMaterial = bs.getSharedObject('regionMaterial')
        
        # send footing messages to spazzes so they know when they're on solid ground
        # eww this should really just be built into the spaz node
        self.rollerMaterial.addActions(
            conditions=('theyHaveMaterial',footingMaterial),
            actions=(('message','ourNode','atConnect','footing',1),
                     ('message','ourNode','atDisconnect','footing',-1)))

        self.spazMaterial.addActions(
            conditions=('theyHaveMaterial',footingMaterial),
            actions=(('message','ourNode','atConnect','footing',1),
                     ('message','ourNode','atDisconnect','footing',-1)))
        # punches
        self.punchMaterial.addActions(
            conditions=('theyAreDifferentNodeThanUs',),
            actions=(('modifyPartCollision','collide',True),
                     ('modifyPartCollision','physical',False),
                     ('message','ourNode','atConnect',_PunchHitMessage())))
        # pickups
        self.pickupMaterial.addActions(
            conditions=(('theyAreDifferentNodeThanUs',),'and',('theyHaveMaterial',objectMaterial)),
            actions=(('modifyPartCollision','collide',True),
                     ('modifyPartCollision','physical',False),
                     ('message','ourNode','atConnect',_PickupMessage())))
        # curse
        self.curseMaterial.addActions(
            conditions=(('theyAreDifferentNodeThanUs',),'and',('theyHaveMaterial',playerMaterial)),
            actions=('message','ourNode','atConnect',_CurseExplodeMessage()))


        self.footImpactSounds = (bs.getSound('footImpact01'), # Flesh characters
                                 bs.getSound('footImpact02'),
                                 bs.getSound('footImpact03'))
        self.metalFootImpactSounds = (bs.getSound('footImpactMetal01'), # Metal characters (mainly robots)
                                 bs.getSound('footImpactMetal02'))

        self.footSkidSound = bs.getSound('skid01')
        self.footRollSound = bs.getSound('scamper01')

        self.rollerMaterial.addActions(
            conditions=('theyHaveMaterial',footingMaterial),
            actions=(('impactSound',self.footImpactSounds,1,0.2),
                     ('skidSound',self.footSkidSound,20,0.3),
                     ('rollSound',self.footRollSound,20,10.0)))

        self.skidSound = bs.getSound('gravelSkid')

        self.spazMaterial.addActions(
            conditions=('theyHaveMaterial',footingMaterial),
            actions=(('impactSound',self.footImpactSounds,20,6),
                     ('skidSound',self.skidSound,2.0,1),
                     ('rollSound',self.skidSound,2.0,1)))

        self.shieldUpSound = bs.getSound('shieldUp')
        self.shieldDownSound = bs.getSound('shieldDown')
        self.shieldHitSound = bs.getSound('shieldHit')
        self.shieldDecaySound = bs.getSound('shieldDecay')
        self.shieldIdleSound = bs.getSound('shieldIdle')
        self.healthPowerupSound = bs.getSound("healthPowerup")

        # we dont want to collide with stuff we're initially overlapping
        # (unless its marked with a special region material)
        self.spazMaterial.addActions(
            conditions=( (('weAreYoungerThan', 51),'and',('theyAreDifferentNodeThanUs',)),
                         'and',('theyDontHaveMaterial',regionMaterial)),
            actions=( ('modifyNodeCollision','collide',False)))
        
        self.spazMedia = {}

    def _getStyle(self,character):
        return appearances[character].style
        
    def _getMedia(self,character):

        t = appearances[character]
        if not self.spazMedia.has_key(character):
            m = self.spazMedia[character] = {
                'jumpSounds':[bs.getSound(s) for s in t.jumpSounds],
                'attackSounds':[bs.getSound(s) for s in t.attackSounds],
                'impactSounds':[bs.getSound(s) for s in t.impactSounds],
                'deathSounds':[bs.getSound(s) for s in t.deathSounds],
                'pickupSounds':[bs.getSound(s) for s in t.pickupSounds],
                'fallSounds':[bs.getSound(s) for s in t.fallSounds],
                'colorTexture':bs.getTexture(t.colorTexture),
                'colorMaskTexture':bs.getTexture(t.colorMaskTexture),
                'headModel':bs.getModel(t.headModel),
                'torsoModel':bs.getModel(t.torsoModel),
                'pelvisModel':bs.getModel(t.pelvisModel),
                'upperArmModel':bs.getModel(t.upperArmModel),
                'foreArmModel':bs.getModel(t.foreArmModel),
                'handModel':bs.getModel(t.handModel),
                'upperLegModel':bs.getModel(t.upperLegModel),
                'lowerLegModel':bs.getModel(t.lowerLegModel),
                'toesModel':bs.getModel(t.toesModel)
            }
        else:
            m = self.spazMedia[character]
        return m

class Spaz(bs.Actor):
    """
    category: Game Flow Classes
    
    Base class for various Spazzes.
    A Spaz is the standard little humanoid character in the game.
    It can be controlled by a player or by AI, and can have
    various different appearances.  The name 'Spaz' is not to be
    confused with the 'Spaz' character in the game, which is just
    one of the skins available for instances of this class.

    Attributes:

       node
          The 'spaz' bs.Node.
    """
    
    pointsMult = 1
    # jasonhu5
    # curseTime = 5000
    curseTime = 12000
    _myBot = None
    # 

    _bombSpotLightPos = None
    _bombSpotLight = None
    _taichiBombs = []
    _taichiBombCenter = None
    _taichiBombSoundSum = 0

    # jasonhu5: used for teleporting
    _teleportal1 = (0.0, 0.0, 0.0)
    _teleportal2 = (0.0, 0.0, 0.0)
    _portal1 = None
    _portal2 = None
    _light1 = None
    _light2 = None

    def spawnPlayerSpaz(self,player,position,_portal1,_portal2,_light1,_light2,hitPoints,angle=None):
        name = player.getName()
        color = player.color
        highlight = player.highlight

        displayColor = bs.getSafeColor(color,targetIntensity=0.75)
        spaz = bs.PlayerSpaz(color=color,
                             highlight=highlight,
                             character=player.character,
                             player=player)
        spaz._portal1 = _portal1
        spaz._portal2 = _portal2
        spaz._light1 = _light1
        spaz._light2 = _light2
        spaz.hitPoints = hitPoints

        # def flashIfHurt(spaz):
            # spaz.node.handleMessage("flash")
        # spaz._timer = bs.Timer(3000, bs.Call(flashIfHurt, spaz))

        player.setActor(spaz)

        # if isinstance(self.getSession(),bs.CoopSession) and self.getMap().getName() in ['Courtyard','Tower D']:
            # mat = self.getMap().preloadData['collideWithWallMaterial']
            # spaz.node.materials += (mat,)
            # spaz.node.rollerMaterials += (mat,)
        
        spaz.node.name = name
        spaz.node.nameColor = displayColor
        spaz.connectControlsToPlayer()
        # self.scoreSet.playerGotNewSpaz(player,spaz)

        # move to the stand position and add a flash of light
        spaz.handleMessage(bs.StandMessage(position,angle if angle is not None else random.uniform(0,360)))
        t = bs.getGameTime()
        bs.playSound(bs.getSound('spawn'),1,position=spaz.node.position)
        # lightColor = bsUtils.getNormalizedColor(color)
        # light = bs.newNode('light',attrs={'color':lightColor})
        # spaz.node.connectAttr('position',light,'position')
        # bsUtils.animate(light,'intensity',{0:0,250:1,500:0})
        # bs.gameTimer(500,light.delete)
        
        return spaz

    # def spawnPlayer(self, player, pos):
    #     x = bs.CoopGameActivity()
    #     s = bs.CoopGameActivity.spawnPlayerSpaz(x, player,position=pos)
    #     if self._preset in ['proEasy','uberEasy']:
    #         s._impactScale = 0.25
    #     s.pickUpPowerupCallback = self._onPlayerPickedUpPowerup

    def _handleTeleport(self, pos):
        n = bs.getCollisionInfo("opposingNode")
        spaz = n.getDelegate()

        if isinstance(spaz, bs.PlayerSpaz):
            _p1 = spaz._portal1
            _p2 = spaz._portal2
            _l1 = spaz._light1
            _l2 = spaz._light2
            _hitPointsBuffer = spaz.hitPoints
            spaz._portal1 = None
            spaz._portal2 = None
            spaz._light1 = None
            spaz._light2 = None

            spaz.handleMessage(bs.DieMessage(immediate=True))
            player = spaz.getPlayer()
            # bs.screenMessage(player.getName())
            if player is None:
                bs.printError('FIXME: getPlayer() should no longer ever be returning None')
                return
            if not player.exists(): return

            respawnTime = 1
            player.gameData['respawnTimer'] = bs.Timer(respawnTime,bs.Call(self.spawnPlayerSpaz,player,pos,_p1,_p2,_l1,_l2,_hitPointsBuffer))
            player.gameData['respawnIcon'] = bs.RespawnIcon(player,respawnTime)
            return

    def _handleTeleport1(self):
        self._handleTeleport(self._teleportal2)

    def _handleTeleport2(self):
        self._handleTeleport(self._teleportal1)
    # 

    defaultBombCount = 1
    defaultBombType = 'normal'
    defaultBlastRadius = 2.0
    defaultBoxingGloves = False
    defaultShields = False

    def __init__(self,color=(1,1,1),highlight=(0.5,0.5,0.5),character="Spaz",sourcePlayer=None,startInvincible=True,canAcceptPowerups=True,powerupsExpire=False):
        """
        Create a new spaz with the requested color, character, etc.
        """
        
        bs.Actor.__init__(self)
        activity = self.getActivity()
        
        factory = self.getFactory()

        self.playBigDeathSound = False

        # translate None into empty player-ref
        if sourcePlayer is None: sourcePlayer = bs.Player(None)

        # scales how much impacts affect us (most damage calcs)
        self._impactScale = 1.0
        
        self.sourcePlayer = sourcePlayer
        self._dead = False
        self._punchPowerScale = gBasePunchPowerScale
        self.fly = bs.getSharedObject('globals').happyThoughtsMode
        self._hockey = activity._map.isHockey
        self._punchedNodes = set()
        self._cursed = False
        self._connectedToPlayer = None

        materials = [factory.spazMaterial,bs.getSharedObject('objectMaterial'),bs.getSharedObject('playerMaterial')]
        rollerMaterials = [factory.rollerMaterial,bs.getSharedObject('playerMaterial')]
        extrasMaterials = []
        
        if canAcceptPowerups:
            pam = bs.Powerup.getFactory().powerupAcceptMaterial
            materials.append(pam)
            rollerMaterials.append(pam)
            extrasMaterials.append(pam)

        media = factory._getMedia(character)
        self.node = bs.newNode(type="spaz",
                               delegate=self,
                               attrs={'color':color,
                                      'highlight':highlight,
                                      'jumpSounds':media['jumpSounds'],
                                      'attackSounds':media['attackSounds'],
                                      'impactSounds':media['impactSounds'],
                                      'deathSounds':media['deathSounds'],
                                      'pickupSounds':media['pickupSounds'],
                                      'fallSounds':media['fallSounds'],
                                      'colorTexture':media['colorTexture'],
                                      'colorMaskTexture':media['colorMaskTexture'],
                                      'headModel':media['headModel'],
                                      'torsoModel':media['torsoModel'],
                                      'pelvisModel':media['pelvisModel'],
                                      'upperArmModel':media['upperArmModel'],
                                      'foreArmModel':media['foreArmModel'],
                                      'handModel':media['handModel'],
                                      'upperLegModel':media['upperLegModel'],
                                      'lowerLegModel':media['lowerLegModel'],
                                      'toesModel':media['toesModel'],
                                      'style':factory._getStyle(character),
                                      'fly':self.fly,
                                      'hockey':self._hockey,
                                      'materials':materials,
                                      'rollerMaterials':rollerMaterials,
                                      'extrasMaterials':extrasMaterials,
                                      'punchMaterials':(factory.punchMaterial,bs.getSharedObject('attackMaterial')),
                                      'pickupMaterials':(factory.pickupMaterial,bs.getSharedObject('pickupMaterial')),
                                      'invincible':startInvincible,
                                      'sourcePlayer':sourcePlayer})
        self.shield = None

        if startInvincible:
            def _safeSetAttr(node,attr,val):
                if node.exists(): setattr(node,attr,val)
            # bs.gameTimer(15000000,bs.Call(_safeSetAttr,self.node,'invincible',False))
            bs.gameTimer(1500,bs.Call(_safeSetAttr,self.node,'invincible',False))

        self.hitPoints = 1000
        self.hitPointsMax = 1000
        #How much HP you can receive from Overdrive powerup
        self.hitPointsOverdrive = 1000
        #How much HP you need to have until you'll be cursed
        self.hitPointsOverdriveTooMuch = 2000
        #How many damage you receive per second if "on fire"
        self.fireDamage = 125
        
        # This value checks how much damage you received. Important for the achievement.
        self.hitPointsAchievement = 0
        
        self.bombCount = self.defaultBombCount
        self._maxBombCount = self.defaultBombCount
        self.bombTypeDefault = self.defaultBombType
        self.bombType = self.bombTypeDefault
        self.landMineCount = 0
        self.grenadeCount = 0
        self.healBombCount = 0
        self.hijumpCount = 0
        self.blastRadius = self.defaultBlastRadius
        self.powerupsExpire = powerupsExpire
        self._punchCooldown = gBasePunchCooldown
        self._hasBoxingGloves = False
        if self.defaultBoxingGloves: self.equipBoxingGloves()
        self.lastPunchTime = 0
        self.frozen = False
        self.burning = False
        self.shattered = False
        self._lastHitTime = None
        self._numTimesHit = 0
        self._bombHeld = False
        if self.defaultShields: 
            try: player = bs.PlayerSpaz.getPlayer(self)
            except Exception: player = None
            self.equipShields(player)

        self._droppedBombCallbacks = []

        # deprecated stuff.. need to make these into lists
        self.punchCallback = None
        self.pickUpPowerupCallback = None

        # jasonhu5
        self._port1Material = bs.Material()
        self._port1Material.addActions(
            conditions=("theyHaveMaterial",bs.getSharedObject('playerMaterial')),
            actions=(("modifyPartCollision","collide",True),
                     ("modifyPartCollision","physical",False),
                     ("call","atConnect",self._handleTeleport1)))

        self._port2Material = bs.Material()
        self._port2Material.addActions(
            conditions=("theyHaveMaterial",bs.getSharedObject('playerMaterial')),
            actions=(("modifyPartCollision","collide",True),
                     ("modifyPartCollision","physical",False),
                     ("call","atConnect",self._handleTeleport2)))
        # 
        
    def lightningPower(self):
        """
        After collecting Overdrive powerup, show some WACKY EFFECTZ, OOOH
        just to highlight the power.
        """  
        self.nova = bs.newNode('light',
                           attrs={'position':self.node.position,
                                  'color': (0.8,0.56,0.8),
                                  'volumeIntensityScale': 0.5})     
                                  
        bs.gameTimer(200,self.nova.delete)    
        bs.emitBGDynamics(position=self.node.position,velocity=self.node.velocity,count=int(8.0+random.random()*45),scale=1.0,spread=3,chunkType='spark');
        
    def onFinalize(self):
        bs.Actor.onFinalize(self)

        # release callbacks/refs so we don't wind up with dependency loops..
        self._droppedBombCallbacks = []
        self.punchCallback = None
        self.pickUpPowerupCallback = None
        
    def addDroppedBombCallback(self,call):
        """
        Add a call to be run whenever this Spaz drops a bomb.
        The spaz and the newly-dropped bomb are passed as arguments.
        """
        self._droppedBombCallbacks.append(call)
                            
    def isAlive(self):
        """
        Method override; returns whether ol' spaz is still kickin'.
        """
        return not self._dead

    @classmethod
    def getFactory(cls):
        """
        Returns the shared bs.SpazFactory object, creating it if necessary.
        """
        activity = bs.getActivity()
        if activity is None: raise Exception("no current activity")
        try: return activity._sharedSpazFactory
        except Exception:
            f = activity._sharedSpazFactory = SpazFactory()
            return f

    def exists(self):
        return self.node.exists()

    def _hideScoreText(self):
        if self._scoreText.exists():
            bs.animate(self._scoreText,'scale',{0:self._scoreText.scale,200:0})

    def setScoreText(self,t,color=(1,1,0.4),flash=False):
        """
        Utility func to show a message momentarily over our spaz that follows him around;
        Handy for score updates and things.
        """
        colorFin = bs.getSafeColor(color)[:3]
        if not self.node.exists(): return
        try: exists = self._scoreText.exists()
        except Exception: exists = False
        if not exists:
            startScale = 0.0
            m = bs.newNode('math',owner=self.node,attrs={'input1':(0,1.4,0),'operation':'add'})
            self.node.connectAttr('torsoPosition',m,'input2')
            self._scoreText = bs.newNode('text',
                                          owner=self.node,
                                          attrs={'text':t,
                                                 'inWorld':True,
                                                 'shadow':1.0,
                                                 'flatness':1.0,
                                                 'color':colorFin,
                                                 'scale':0.02,
                                                 'hAlign':'center'})
            m.connectAttr('output',self._scoreText,'position')
        else:
            self._scoreText.color = colorFin
            startScale = self._scoreText.scale
            self._scoreText.text = t
        if flash:
            combine = bs.newNode("combine",owner=self._scoreText,attrs={'size':3})
            sc = 1.8
            offs = 0.5
            t = 300
            for i in range(3):
                c1 = offs+sc*colorFin[i]
                c2 = colorFin[i]
                bs.animate(combine,'input'+str(i),{0.5*t:c2,
                                                   0.75*t:c1,
                                                   1.0*t:c2})
            combine.connectAttr('output',self._scoreText,'color')
            
        bs.animate(self._scoreText,'scale',{0:startScale,200:0.02})
        self._scoreTextHideTimer = bs.Timer(1000,bs.WeakCall(self._hideScoreText))

        
    def moveInstantly(self, p, v, lr, ud, count):
        const_cnt_bomb = 20
        const_cnt_total = 23
        const_blast_radius = 0.0
        const_per_angle = 30

        # px = 0.0 + lr * 0.1 + v[0] * 0.2
        # py = 0.0 - 1.2
        # pz = 0.0 - ud * 0.1 + v[2] * 0.2
        px = 0.0
        py = 0.0 - 1.3
        pz = 0.0

        newPos = (p[0] + px, p[1] + py, p[2] + pz)

        def _doEmit():
            position = (p[0],p[1] + 0.0,p[2])
            velocity = (speedScale * math.sin(math.pi / 4 * i), 0.0, speedScale * math.cos(math.pi / 4 * i))
            bs.emitBGDynamics(position=position,velocity=velocity,count=int(1.0+random.random()*4),emitType='tendrils',tendrilType='smoke')
            bs.emitBGDynamics(position=position,emitType='distortion',spread=1.0)
         # looks better if we delay a bit

        if (count < const_cnt_bomb):
            speedScale = 3.0
            for i in range(4):
                bs.gameTimer(50,_doEmit)

        # if (count < const_cnt_bomb):
        #     speedScale = 3.0
        #     for i in range(4):
        #         bomb = bs.Bomb(position=(p[0],p[1] + 0.0,p[2]),
        #             velocity=(speedScale * math.sin(math.pi / 4 * i), 0.0, speedScale * math.cos(math.pi / 4 * i)),
        #             bombType='healing',
        #             blastRadius=const_blast_radius,
        #             sourcePlayer=self.sourcePlayer,
        #             owner=self.node).autoRetain()

        # self._player.actor.handleMessage(bs.StandMessage(newPos, (-const_per_angle * count) % 360))

        if (count < const_cnt_total):
            self._timerMoveInstantly = bs.Timer(10, bs.WeakCall(self.moveInstantly, p, v, lr, ud, count + 1))
        else:
            bs.Blast(position=self._taichiBombCenter,velocity=(0,0,0),
                blastRadius=5.0,blastType='sticky',sourcePlayer=self._player,hitType='explosion',hitSubType='sticky').autoRetain()
            pos = self._taichiBombCenter
            v = (0.0,0.0,0.0)
            self.node.handleMessage("impulse",pos[0],pos[1],pos[2],
                                    v[0],v[1],v[2],
                                    10000.0,10.0,5.0,0,v[0], v[1], v[2])

    def circleBomb(self, p, count):
        const_cnt_total = 64
        const_blast_radius = 0.5
        const_no_of_bombs = 4
        const_center_dist = 0.0
        unit = 0.3
        r = 4.0
        scorchRadius = 0.2

        offset0 = math.sin(math.pi / const_cnt_total * count) * (const_center_dist + unit * r)
        offset1 = -0.7
        offset2 = math.cos(math.pi / const_cnt_total * count) * (const_center_dist + unit * r)

        for i in [0, 1]:
            off0 = offset0
            off1 = offset1
            off2 = offset2
            
            if i == 1:
                off0 = -offset0
                off2 = -offset2
                scorch = bs.newNode('scorch',
                        attrs={'position':(off0 + p[0] ,p[1] + off1, off2 + p[2]),'size':scorchRadius*0.5,'big':False})
                scorch.color = (2,2,2)
            else:
                scorch = bs.newNode('scorch',
                        attrs={'position':(off0 + p[0] ,p[1] + off1, off2 + p[2]),'size':scorchRadius*0.5,'big':False})

            self._taichiBombs.append(scorch)
            bsUtils.animate(scorch,"presence",{1000:1, 6000:0})
            bs.gameTimer(6000,scorch.delete)
            
            # bomb = bs.Bomb(position=(off0 + p[0] ,p[1] + off1, off2 + p[2]),
            #     velocity=(0.0, 0.0, 0.0),
            #     bombType='sticky',
            #     blastRadius=const_blast_radius,
            #     sourcePlayer=self.sourcePlayer,
            #     owner=self.node).autoRetain()

        if (count < const_cnt_total):
            self._timer = bs.Timer(10, bs.WeakCall(self.circleBomb, p, count + 1))
        else:
            c0 = (p[0], p[1], p[2] + r/2 * unit)
            c1 = (p[0], p[1], p[2] - r/2 * unit)
            self._timer = bs.Timer(2, bs.WeakCall(self.taichiBomb, c0, c1, 0))
            for i in [0, 1]:
                p = c0 if i == 0 else c1
                for x in range(8):
                    if i == 0:
                        p = c0
                        scorch = bs.newNode('scorch',
                                attrs={'position':(p[0] ,p[1] + offset1, p[2]),'size':scorchRadius*1.0,'big':False})
                    else:
                        p = c1
                        scorch = bs.newNode('scorch',
                                attrs={'position':(p[0] ,p[1] + offset1, p[2]),'size':scorchRadius*1.0,'big':False})
                        scorch.color = (2,2,2)
                    self._taichiBombs.append(scorch)
                    bsUtils.animate(scorch,"presence",{1000:1, 6000:0})
                    bs.gameTimer(6000,scorch.delete)
                # for x in range(4):
                    # bomb = bs.Bomb(position=(p[0] ,p[1] + offset1, p[2]),
                    #     velocity=(0.0, 0.0, 0.0),
                    #     bombType='sticky',
                    #     blastRadius=0.7,
                    #     sourcePlayer=self.sourcePlayer,
                    #     owner=self.node).autoRetain()

    def taichiBomb(self, c0, c1, count):
        const_cnt_total = 32
        const_blast_radius = 0.3
        const_no_of_bombs = 4
        const_center_dist = 0.0
        unit = 0.3
        r = 2
        scorchRadius = 0.2

        offset0 = math.sin(math.pi / const_cnt_total * count) * (const_center_dist + unit * r)
        offset1 = -0.7
        offset2 = math.cos(math.pi / const_cnt_total * count) * (const_center_dist + unit * r)

        for i in [0, 1]:
            off0 = offset0
            off1 = offset1
            off2 = offset2
            p = c0
            if i == 1:
                p = c1
                off0 = -offset0
                off2 = -offset2
                scorch = bs.newNode('scorch',
                        attrs={'position':(off0 + p[0] ,p[1] + off1, off2 + p[2]),'size':scorchRadius*0.5,'big':False})
            else:
                scorch = bs.newNode('scorch',
                        attrs={'position':(off0 + p[0] ,p[1] + off1, off2 + p[2]),'size':scorchRadius*0.5,'big':False})
                scorch.color = (2,2,2)

            self._taichiBombs.append(scorch)
            bsUtils.animate(scorch,"presence",{1000:1, 6000:0})
            bs.gameTimer(6000,scorch.delete)
            
            # bomb = bs.Bomb(position=(off0 + p[0] ,p[1] + off1, off2 + p[2]),
            #     velocity=(0.0, 0.0, 0.0),
            #     bombType='sticky',
            #     blastRadius=const_blast_radius,
            #     sourcePlayer=self.sourcePlayer,
            #     owner=self.node).autoRetain()

        if (count < const_cnt_total):
            self._timer = bs.Timer(10, bs.WeakCall(self.taichiBomb, c0, c1, count + 1))
        else:
            v = self.node.velocity
            p = self.node.positionForward
            # self.moveInstantly(p, v, self.node.moveLeftRight, self.node.moveUpDown, 1)
            self.taichiRotate(0)

    def taichiRotate(self, count):
        const_cnt_total = 300
        rotation_angle = (count * -1.0) / 4.0

        pp = self.node.positionForward

        blast_flag = True

        def rotate(origin, point, angle, blast_flag):
            from math import sqrt, pow
            ox, oh, oy = origin
            px, ph, py = point

            qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
            qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)

            r_ext_rate = 2.0
            const_blast_radius = 3.0
            blastPos = (
                r_ext_rate * qx - ox + (pp[0] - ox), 
                ph + (pp[1] - oh), 
                r_ext_rate * qy - oy + (pp[2] - oy)
            )

            # dist = sqrt(pow(ox - px, 2) + pow(oh - ph, 2) + pow(oy - py, 2))
            if blast_flag:
                bs.Blast(position=blastPos,velocity=(px - ox,ph - oh,py - oy),
                    blastRadius=const_blast_radius,blastType='sticky',sourcePlayer=self._player,hitType='explosion',hitSubType='sticky').autoRetain()

            return (qx + (pp[0] - ox), ph + (pp[1] - oh), qy + (pp[2] - oy))

        self._taichiBombSoundSum += count
        # print(str(self._taichiBombSoundSum))
        if self._taichiBombSoundSum > 3500:
            self._taichiBombSoundSum = 0
            bs.playSound(self.getFactory().hissSound, position=self._taichiBombCenter)

        if count == const_cnt_total - 20:
            bs.playSound(bs.getSound('taichiSound'), volume=1.0, position=self._taichiBombCenter)

        for s in self._taichiBombs:
            if not s.exists():
                continue
            p = getattr(s, "position")
            if blast_flag:
                newPos = rotate(self._taichiBombCenter, p, math.radians(rotation_angle), blast_flag)
                blast_flag = False
            else:
                newPos = rotate(self._taichiBombCenter, p, math.radians(rotation_angle), blast_flag)

            setattr(s, "position", (newPos))

        self._taichiBombCenter = pp

        if (count < const_cnt_total):
            self._timer = bs.Timer(10, bs.WeakCall(self.taichiRotate, count + 1))
        else:
            light = bs.newNode('light',
                           attrs={'position':self._taichiBombCenter
                           ,
                                  'color': (2,2,2), #(0.6,0.6,1.0) if self.blastType == 'ice' else (1,0.3,0.1),
                                  'volumeIntensityScale': 10.0})
            s = random.uniform(0.6,0.9)
            iScale = 1.6
            lightRadius = 0.6
            bsUtils.animate(light,"intensity",{0:2.0*iScale, int(s*20):0.1*iScale, int(s*25):0.2*iScale, int(s*50):50.0*iScale, int(s*60):5.0*iScale, int(s*80):4.0*iScale, int(s*200):0.6*iScale, int(s*1500):10.00*iScale, int(s*4000):0.0})
            bsUtils.animate(light,"radius",{0:lightRadius*0.05, int(s*1300):lightRadius*0.25, int(s*1500):lightRadius*0.00})
            bs.gameTimer(int(s*10000),light.delete)

            # self.moveInstantly(self._taichiBombCenter, self.node.velocity, self.node.moveLeftRight, self.node.moveUpDown, 1)
            self._timer = bs.Timer(1000, bs.WeakCall(self.moveInstantly, self._taichiBombCenter, self.node.velocity, self.node.moveLeftRight, self.node.moveUpDown, 1))

    def onJumpPress(self):
        """
        Called to 'press jump' on this spaz;
        used by player or AI connections.
        """
        if not self.node.exists(): return
        self.node.jumpPressed = True

        # jaosnhu5
        # p = self.node.positionForward
        # v = self.node.velocity

        # lr = self.node.moveLeftRight
        # ud = self.node.moveUpDown

        # px = 0.0 + lr * 0.2 + v[0] * 0.5
        # py = 0.0 - 1.3
        # pz = 0.0 - ud * 0.2 + v[2] * 0.5
        # newPos = (p[0] + px, p[1] + py, p[2] + pz)
        # self._player.actor.handleMessage(bs.StandMessage(newPos, random.uniform(0,360)))
        # 


    def onJumpRelease(self):
        """
        Called to 'release jump' on this spaz;
        used by player or AI connections.
        """
        if not self.node.exists(): return
        self.node.jumpPressed = False

    def onPickUpPress(self):
        """
        Called to 'press pick-up' on this spaz;
        used by player or AI connections.
        """
        if not self.node.exists(): return
        self.node.pickUpPressed = True

    def onPickUpRelease(self):
        """
        Called to 'release pick-up' on this spaz;
        used by player or AI connections.
        """
        if not self.node.exists(): return
        self.node.pickUpPressed = False

    def _onHoldPositionPress(self):
        """
        Called to 'press hold-position' on this spaz;
        used for player or AI connections.
        """
        if not self.node.exists(): return
        self.node.holdPositionPressed = True

    def _onHoldPositionRelease(self):
        """
        Called to 'release hold-position' on this spaz;
        used for player or AI connections.
        """
        if not self.node.exists(): return
        self.node.holdPositionPressed = False

    def onPunchPress(self):
        """
        Called to 'press punch' on this spaz;
        used for player or AI connections.
        """
        if not self.node.exists() or self.frozen or self.node.knockout > 0.0: return
        
        if self.punchCallback is not None:
            self.punchCallback(self)
        t = bs.getGameTime()
        self._punchedNodes = set() # reset this..
        if t - self.lastPunchTime > self._punchCooldown:
            self.lastPunchTime = t
            self.node.punchPressed = True
            if not self.node.holdNode.exists():
                punches = self.getFactory().swishSounds
                punch = punches[random.randrange(len(punches))]
                bs.gameTimer(100,bs.WeakCall(self._safePlaySound,punch,0.6))

        # jasonhu5
        # for i in [v for v in dir(self.node) if not callable(getattr(self.node, v))]:
            # print('\n'+str(i)+':') 
            # print('\n'+str(getattr(self.node, i)))
            #     if str(i) == 'positionCenter':
            #         pc = getattr(self.node, i)
            #     if str(i) == 'positionForward':
            #         pf = getattr(self.node, i)
            # pd = (pf[0] - pc[0], pf[1] - pc[1], pf[2] - pc[2])
            # print(str(pd))
        # 
                

    def _safePlaySound(self,sound,volume):
        """
        Plays a sound at our position if we exist.
        """
        if self.node.exists():
            bs.playSound(sound,volume,self.node.position)
        
    def onPunchRelease(self):
        """
        Called to 'release punch' on this spaz;
        used for player or AI connections.
        """
        if not self.node.exists(): return
        self.node.punchPressed = False

    def onBombPress(self):
        """
        Called to 'press bomb' on this spaz;
        used for player or AI connections.
        """
        if not self.node.exists(): return
        
        if self._dead or self.frozen: return
        if self.node.knockout > 0.0: return
        self.node.bombPressed = True
        if not self.node.holdNode.exists(): self.dropBomb()

        # jasonhu5 taichi
        # v = self.node.velocity
        # p = self.node.positionForward
        
        # self._taichiBombCenter = p
        # self._taichiBombs = []
        # self._taichiBombSoundSum = 0
        # self.circleBomb(p, 0)
        #

    def onBombRelease(self):
        """
        Called to 'release bomb' on this spaz; 
        used for player or AI connections.
        """
        if not self.node.exists(): return
        self.node.bombPressed = False

    def onRun(self,value):
        """
        Called to 'press run' on this spaz;
        used for player or AI connections.
        """
        if not self.node.exists(): return
        self.node.run = value

    def onFlyPress(self):
        """
        Called to 'press fly' on this spaz;
        used for player or AI connections.
        """
        if not self.node.exists(): return
        self.node.flyPressed = True

    def onFlyRelease(self):
        """
        Called to 'release fly' on this spaz;
        used for player or AI connections.
        """
        if not self.node.exists(): return
        self.node.flyPressed = False

    def onMove(self,x,y):
        """
        Called to set the joystick amount for this spaz;
        used for player or AI connections.
        """
        if not self.node.exists(): return
        self.node.handleMessage("move",x,y)
        
    def onMoveUpDown(self,value):
        """
        Called to set the up/down joystick amount on this spaz;
        used for player or AI connections.
        value will be between -32768 to 32767
        WARNING: deprecated; use onMove instead.
        """
        if not self.node.exists(): return
        self.node.moveUpDown = value 

    def onMoveLeftRight(self,value):
        """
        Called to set the left/right joystick amount on this spaz;
        used for player or AI connections.
        value will be between -32768 to 32767
        WARNING: deprecated; use onMove instead.
        """
        if not self.node.exists(): return
        self.node.moveLeftRight = value

    def onPunched(self,damage):
        """
        Called when this spaz gets punched.
        """
        pass

    def getDeathPoints(self,how):
        'Get the points awarded for killing this spaz'
        numHits = float(max(1,self._numTimesHit))
        # base points is simply 10 for 1-hit-kills and 5 otherwise
        importance = 2 if numHits < 2 else 1
        return ((10 if numHits < 2 else 5) * self.pointsMult,importance)

    def curse(self):
        """
        Give this poor spaz a curse;
        he will explode in curseTime/1000 seconds.
        """
        if not self._cursed:
            if self.healBombCount != 0: # Don't curse the players that have Healing Bombs in their inventory. Instead of cursing, remove one from the stock.
                self.setHealBombCount(self.healBombCount-1)
            else:
                factory = self.getFactory()
                self._cursed = True
                if bs.getConfig().get('Offensive Curse Sound', True):
                    self.sound = bs.newNode('sound',owner=self.node,attrs={'sound':factory.curseOffensiveSound,'volume':1.0})
                else:
                    self.sound = bs.newNode('sound',owner=self.node,attrs={'sound':factory.curseSound,'volume':1.0})
                self.node.connectAttr('position',self.sound,'position')
                # add the curse material..
                for attr in ['materials','rollerMaterials']:
                    materials = getattr(self.node,attr)
                    if not factory.curseMaterial in materials:
                        setattr(self.node,attr,materials + (factory.curseMaterial,))
                # -1 specifies no time limit
                if self.curseTime == -1:
                    self.node.curseDeathTime = -1
                else:
                    self.node.curseDeathTime = bs.getGameTime()+self.curseTime
                    self.curseExplodeTimer = bs.Timer(self.curseTime,bs.WeakCall(self.curseExplode))
        else:
            if not self.curseTime == -1:
                self.node.curseDeathTime = bs.getGameTime()+self.curseTime
                self.curseExplodeTimer = bs.Timer(self.curseTime,bs.WeakCall(self.curseExplode))
            
    def equipBoxingGloves(self):
        """
        Give this spaz some boxing gloves.
        """
        activity = self.getActivity()
        factory = self.getFactory()
        
        def _safeSetAttr(node,attr,val):
            if node.exists(): setattr(node,attr,val)
        if not activity._map.isHockey:
            bs.gameTimer(1,bs.Call(_safeSetAttr,self.node,'hockey',False))
        self.node.boxingGloves = 1
        self._hasBoxingGloves = True
        self._punchPowerScale = 1.9
        self._punchCooldown = 750
        
    def equipSpeed(self):
        """
        Give this spaz speed boots.
        """
        factory = self.getFactory()
        def _safeSetAttr(node,attr,val):
            if node.exists(): setattr(node,attr,val)
        bs.gameTimer(1,bs.Call(_safeSetAttr,self.node,'hockey',True))
        bs.playSound(factory.speedUpSound,position=self.node.position)
        self._hasBoxingGloves = False
        self.node.boxingGloves = 0
        self._punchPowerScale = 1.1
        self._punchCooldown = 350

    def equipShields(self,player):
        """
        Give this spaz a nice energy shield.
        """

        if not self.node.exists(): raise Exception('Can\'t equip shields; no node.')
        
        factory = self.getFactory()
        if player is not None:
            if self.shield is None: 
                if isinstance(bs.getSession(),bs.TeamsSession): # Color the shields based on the team you're in (if it's a team game, that is)
                    playerTeam = player.getTeam().getID()
                    if playerTeam == 0:
                        self.shield = bs.newNode('shield',owner=self.node,
                                        attrs={'color':(0.2,0.2,5.0),'radius':1.3})
                    elif playerTeam == 1:
                        self.shield = bs.newNode('shield',owner=self.node,
                                        attrs={'color':(3.0,0.2,0.2),'radius':1.3})
                    else:
                        self.shield = bs.newNode('shield',owner=self.node,
                                        attrs={'color':(0.3,0.2,2.0),'radius':1.3})
                else:
                    self.shield = bs.newNode('shield',owner=self.node,
                                        attrs={'color':(0.3,0.2,2.0),'radius':1.3})
                self.node.connectAttr('positionCenter',self.shield,'position')
                self.shieldSound = bs.newNode('sound',owner=self.node,attrs={'sound':factory.shieldIdleSound,'volume':0.55})
                self.node.connectAttr('position',self.shieldSound,'position')
            else:
                if self.shieldHitPoints == 1:
                    self.shield.delete()
                    if isinstance(bs.getSession(),bs.TeamsSession): # Color the shields based on the team you're in (if it's a team game, that is)
                        playerTeam = player.getTeam().getID()
                        if playerTeam == 0:
                            self.shield = bs.newNode('shield',owner=self.node,
                                            attrs={'color':(0.2,0.2,5.0),'radius':1.3})
                        elif playerTeam == 1:
                            self.shield = bs.newNode('shield',owner=self.node,
                                            attrs={'color':(3.0,0.2,0.2),'radius':1.3})
                        else:
                            self.shield = bs.newNode('shield',owner=self.node,
                                            attrs={'color':(0.3,0.2,2.0),'radius':1.3})
                    else:
                            self.shield = bs.newNode('shield',owner=self.node,
                                                attrs={'color':(0.3,0.2,2.0),'radius':1.3})
                    self.node.connectAttr('positionCenter',self.shield,'position')
                    self.shieldSound = bs.newNode('sound',owner=self.node,attrs={'sound':factory.shieldIdleSound,'volume':0.55})
                    self.node.connectAttr('position',self.shieldSound,'position')
            # Outside Coop sessions, increase the shield's health, to compensate for the decaying mechanic. Since in Coop sessions the shield doesn't decay, I leave its value to default 600.
            if not isinstance(bs.getSession(),bs.CoopSession): 
                self.shieldHitPoints = self.shieldHitPointsMax = 800
            else:
                self.shieldHitPoints = self.shieldHitPointsMax = 600
            self.shield.hurt = 0
            bs.playSound(factory.shieldUpSound,1.0,position=self.node.position)
            if not isinstance(bs.getSession(),bs.CoopSession):
                self.shieldDecayTimer = bs.Timer(20000,bs.WeakCall(self.shieldDecay)) # Only decay shields outside of Coop sessions
        else: # If the player is not given
            if self.shield is None: 
                self.shield = bs.newNode('shield',owner=self.node,
                                        attrs={'color':(0.3,0.2,2.0),'radius':1.3})
                self.node.connectAttr('positionCenter',self.shield,'position')
                self.shieldSound = bs.newNode('sound',owner=self.node,attrs={'sound':factory.shieldIdleSound,'volume':0.55})
                self.node.connectAttr('position',self.shieldSound,'position')
            else:
                if self.shieldHitPoints == 1:
                    self.shield.delete()
                self.shield = bs.newNode('shield',owner=self.node,
                                        attrs={'color':(0.3,0.2,2.0),'radius':1.3})
                self.node.connectAttr('positionCenter',self.shield,'position')
                self.shieldSound = bs.newNode('sound',owner=self.node,attrs={'sound':factory.shieldIdleSound,'volume':0.55})
                self.node.connectAttr('position',self.shieldSound,'position')
            # Outside Coop sessions, increase the shield's health, to compensate for the decaying mechanic. Since in Coop sessions the shield doesn't decay, I leave its value to default 600.
            if not isinstance(bs.getSession(),bs.CoopSession): 
                self.shieldHitPoints = self.shieldHitPointsMax = 800
            else:
                self.shieldHitPoints = self.shieldHitPointsMax = 600
            self.shield.hurt = 0
            bs.playSound(factory.shieldUpSound,1.0,position=self.node.position)
            if not isinstance(bs.getSession(),bs.CoopSession):
                self.shieldDecayTimer = bs.Timer(20000,bs.WeakCall(self.shieldDecay)) # Only decay shields outside of Coop sessions
        
    def shieldDecay(self):
        factory = self.getFactory()
        if self.shield is not None:
            t = self.node.position
            self.shieldHitPoints = 1
            self.shield.delete()
            self.shieldSound.delete()
            self.shield = None
            self.shield = bs.newNode('shield',owner=self.node,
                                    attrs={'color':(0.7,0.7,0.7),'radius':1.0})
            self.node.connectAttr('positionCenter',self.shield,'position')
            bs.playSound(self.getFactory().shieldDecaySound,1.0,position=self.node.position)
            # emit some cool lookin sparks when the shield decays
            bs.emitBGDynamics(position=(t[0],t[1]+0.9,t[2]),
                            velocity=self.node.velocity,
                            count=random.randrange(30,50),scale=0.3,spread=1,chunkType='spark')
            self.shield.hurt = 1.0
        
    def handleMessage(self,m):
        import bsInternal
        self._handleMessageSanityCheck()

        if isinstance(m,bs.PickedUpMessage):
            self.node.handleMessage("hurtSound")
            self.node.handleMessage("pickedUp")
            # this counts as a hit
            self._numTimesHit += 1

        elif isinstance(m,bs.ShouldShatterMessage):
            # eww; seems we have to do this in a timer or it wont work right
            # (since we're getting called from within update() perhaps?..)
            bs.gameTimer(1,bs.WeakCall(self.shatter))

        elif isinstance(m,bs.ImpactDamageMessage):
            # eww; seems we have to do this in a timer or it wont work right
            # (since we're getting called from within update() perhaps?..)
            bs.gameTimer(1,bs.WeakCall(self._hitSelf,m.intensity))

        elif isinstance(m,bs.PowerupMessage):
            self.scale = 1.3 # Powerup Notification text size
            if self._dead: return True
            if self.pickUpPowerupCallback is not None:
                self.pickUpPowerupCallback(self)

            if (m.powerupType == 'tripleBombs'):
                tex = bs.Powerup.getFactory().texBomb
                self._flashBillboard(tex)
                self.setBombCount(3)
                self.blastRadius = self.defaultBlastRadius
                if bs.getConfig().get('Powerup Popups', True):
                    bsUtils.PopupText((bs.Lstr(resource='tripleBombs')),
                                            color=(1,1,0),
                                            scale=self.scale,
                                            position=self.node.position).autoRetain()
                if self.powerupsExpire:
                    self.node.miniBillboard1Texture = tex
                    t = bs.getGameTime()
                    self.node.miniBillboard1StartTime = t
                    self.node.miniBillboard1EndTime = t+gPowerupWearOffTime
                    self._multiBombWearOffFlashTimer = bs.Timer(gPowerupWearOffTime-2000,bs.WeakCall(self._multiBombWearOffFlash))
                    self._multiBombWearOffTimer = bs.Timer(gPowerupWearOffTime,bs.WeakCall(self._multiBombWearOff))
            elif (m.powerupType == 'blastBuff'):
                tex = bs.Powerup.getFactory().texBlast
                self._flashBillboard(tex)
                self.setBombCount(self.defaultBombCount)
                self.blastRadius = 2.2
                if bs.getConfig().get('Powerup Popups', True):
                    bsUtils.PopupText((bs.Lstr(resource='blastBuff')),
                                            color=(1,1,0),
                                            scale=self.scale,
                                            position=self.node.position).autoRetain()
                if self.powerupsExpire:
                    self.node.miniBillboard1Texture = tex
                    t = bs.getGameTime()
                    self.node.miniBillboard1StartTime = t
                    self.node.miniBillboard1EndTime = t+gPowerupWearOffTime
                    self._multiBombWearOffFlashTimer = bs.Timer(gPowerupWearOffTime-2000,bs.WeakCall(self._blastBuffWearOffFlash))
                    self._multiBombWearOffTimer = bs.Timer(gPowerupWearOffTime,bs.WeakCall(self._blastBuffWearOff))
            elif m.powerupType == 'landMines':
                self.setGrenadeCount(min(0,4))
                self.setHealBombCount(min(0,2))
                self.setHijumpCount(min(0,6))
                self.setLandMineCount(min(self.landMineCount+3,3))
                if bs.getConfig().get('Powerup Popups', True):
                    bsUtils.PopupText((bs.Lstr(resource='landMine')),
                                            color=(0.1,0.7,0),
                                            scale=self.scale,
                                            position=self.node.position).autoRetain()
            elif m.powerupType == 'grenades':
                self.setHealBombCount(min(0,2))
                self.setLandMineCount(min(0,3))
                self.setHijumpCount(min(0,6))
                self.setGrenadeCount(min(self.grenadeCount+2,4))
                if bs.getConfig().get('Powerup Popups', True):
                    bsUtils.PopupText((bs.Lstr(resource='grenade')),
                                            color=(0.57,0.82,0.6),
                                            scale=self.scale,
                                            position=self.node.position).autoRetain()
            elif m.powerupType == 'hijump':
                self.setHealBombCount(min(0,2))
                self.setLandMineCount(min(0,3))
                self.setGrenadeCount(min(0,4))
                self.setHijumpCount(min(self.hijumpCount+3,6))
                if bs.getConfig().get('Powerup Popups', True):
                    bsUtils.PopupText((bs.Lstr(resource='hijump')),
                                            color=(1,0.01,0.95),
                                            scale=self.scale,
                                            position=self.node.position).autoRetain()
            elif m.powerupType == 'healBombs':
                self.setGrenadeCount(min(0,4))
                self.setLandMineCount(min(0,3))
                self.setHijumpCount(min(0,6))
                self.setHealBombCount(min(self.healBombCount+1,2))
                if bs.getConfig().get('Powerup Popups', True):
                    bsUtils.PopupText((bs.Lstr(resource='healBomb')),
                                            color=(1,0.4,0.7),
                                            scale=self.scale,
                                            position=self.node.position).autoRetain()
            elif m.powerupType == 'impactBombs':
                self.bombType = 'impact'
                tex = self._getBombTypeTex()
                self._flashBillboard(tex)
                if bs.getConfig().get('Powerup Popups', True):
                    bsUtils.PopupText((bs.Lstr(resource='impactBomb')),
                                            color=(0.6,0.6,0.6),
                                            scale=self.scale,
                                            position=self.node.position).autoRetain()
                if self.powerupsExpire:
                    self.node.miniBillboard2Texture = tex
                    t = bs.getGameTime()
                    self.node.miniBillboard2StartTime = t
                    self.node.miniBillboard2EndTime = t+gPowerupWearOffTime
                    self._bombWearOffFlashTimer = bs.Timer(gPowerupWearOffTime-2000,bs.WeakCall(self._bombWearOffFlash))
                    self._bombWearOffTimer = bs.Timer(gPowerupWearOffTime,bs.WeakCall(self._bombWearOff))
            elif m.powerupType == 'knockerBombs':
                self.bombType = 'knocker'
                tex = self._getBombTypeTex()
                self._flashBillboard(tex)
                if bs.getConfig().get('Powerup Popups', True):
                    bsUtils.PopupText((bs.Lstr(resource='knockerBomb')),
                                            color=(0.0,0.0,1.0),
                                            scale=self.scale,
                                            position=self.node.position).autoRetain()
                if self.powerupsExpire:
                    self.node.miniBillboard2Texture = tex
                    t = bs.getGameTime()
                    self.node.miniBillboard2StartTime = t
                    self.node.miniBillboard2EndTime = t+gPowerupWearOffTime
                    self._bombWearOffFlashTimer = bs.Timer(gPowerupWearOffTime-2000,bs.WeakCall(self._bombWearOffFlash))
                    self._bombWearOffTimer = bs.Timer(gPowerupWearOffTime,bs.WeakCall(self._bombWearOff))
            elif m.powerupType == 'stickyBombs':
                self.bombType = 'sticky'
                tex = self._getBombTypeTex()
                self._flashBillboard(tex)
                if bs.getConfig().get('Powerup Popups', True):
                    bsUtils.PopupText((bs.Lstr(resource='stickyBomb')),
                                            color=(0,1,0),
                                            scale=self.scale,
                                            position=self.node.position).autoRetain()
                if self.powerupsExpire:
                    self.node.miniBillboard2Texture = tex
                    t = bs.getGameTime()
                    self.node.miniBillboard2StartTime = t
                    self.node.miniBillboard2EndTime = t+gPowerupWearOffTime
                    self._bombWearOffFlashTimer = bs.Timer(gPowerupWearOffTime-2000,bs.WeakCall(self._bombWearOffFlash))
                    self._bombWearOffTimer = bs.Timer(gPowerupWearOffTime,bs.WeakCall(self._bombWearOff))
            # jasonhu5
            elif m.powerupType == 'overPower':
                self.bombType = 'overPowerBomb'
                tex = self._getBombTypeTex()
                self._flashBillboard(tex)
                if bs.getConfig().get('Powerup Popups', True):
                    bsUtils.PopupText((bs.Lstr(resource='stickyBomb')),
                                            color=(0,1,0),
                                            scale=self.scale,
                                            position=self.node.position).autoRetain()
                if self.powerupsExpire:
                    self.node.miniBillboard2Texture = tex
                    t = bs.getGameTime()
                    self.node.miniBillboard2StartTime = t
                    self.node.miniBillboard2EndTime = t+gPowerupWearOffTime
                    self._bombWearOffFlashTimer = bs.Timer(gPowerupWearOffTime-2000,bs.WeakCall(self._bombWearOffFlash))
                    self._bombWearOffTimer = bs.Timer(gPowerupWearOffTime,bs.WeakCall(self._bombWearOff))
            # 
            elif m.powerupType == 'rangerBombs':
                self.bombType = 'ranger'
                tex = self._getBombTypeTex()
                self._flashBillboard(tex)
                if bs.getConfig().get('Powerup Popups', True):
                    bsUtils.PopupText((bs.Lstr(resource='rangerBomb')),
                                            color=(1,1,0.5),
                                            scale=self.scale,
                                            position=self.node.position).autoRetain()
                if self.powerupsExpire:
                    self.node.miniBillboard2Texture = tex
                    t = bs.getGameTime()
                    self.node.miniBillboard2StartTime = t
                    self.node.miniBillboard2EndTime = t+gPowerupWearOffTime
                    self._bombWearOffFlashTimer = bs.Timer(gPowerupWearOffTime-2000,bs.WeakCall(self._bombWearOffFlash))
                    self._bombWearOffTimer = bs.Timer(gPowerupWearOffTime,bs.WeakCall(self._bombWearOff))
            elif m.powerupType == 'combatBombs':
                self.bombType = 'combat'
                tex = self._getBombTypeTex()
                self._flashBillboard(tex)
                if bs.getConfig().get('Powerup Popups', True):
                    bsUtils.PopupText((bs.Lstr(resource='combatBomb')),
                                            color=(0,1,1),
                                            scale=self.scale,
                                            position=self.node.position).autoRetain()
                if self.powerupsExpire:
                    self.node.miniBillboard2Texture = tex
                    t = bs.getGameTime()
                    self.node.miniBillboard2StartTime = t
                    self.node.miniBillboard2EndTime = t+gPowerupWearOffTime
                    self._bombWearOffFlashTimer = bs.Timer(gPowerupWearOffTime-2000,bs.WeakCall(self._bombWearOffFlash))
                    self._bombWearOffTimer = bs.Timer(gPowerupWearOffTime,bs.WeakCall(self._bombWearOff))
            elif m.powerupType == 'dynamitePack':
                self.bombType = 'dynamite'
                tex = self._getBombTypeTex()
                self._flashBillboard(tex)
                if bs.getConfig().get('Powerup Popups', True):
                    bsUtils.PopupText((bs.Lstr(resource='dynamitePack')),
                                            color=(1,0,0),
                                            scale=self.scale,
                                            position=self.node.position).autoRetain()
                if self.powerupsExpire:
                    self.node.miniBillboard2Texture = tex
                    t = bs.getGameTime()
                    self.node.miniBillboard2StartTime = t
                    self.node.miniBillboard2EndTime = t+gPowerupWearOffTime
                    self._bombWearOffFlashTimer = bs.Timer(gPowerupWearOffTime-2000,bs.WeakCall(self._bombWearOffFlash))
                    self._bombWearOffTimer = bs.Timer(gPowerupWearOffTime,bs.WeakCall(self._bombWearOff))
            elif m.powerupType == 'punch':
                self._hasBoxingGloves = True
                tex = bs.Powerup.getFactory().texPunch
                self._flashBillboard(tex)
                self.equipBoxingGloves()
                if bs.getConfig().get('Powerup Popups', True):
                    bsUtils.PopupText((bs.Lstr(resource='punch')),
                                            color=(1,0.3,0.3),
                                            scale=self.scale,
                                            position=self.node.position).autoRetain()
                if self.powerupsExpire:
                    self.node.boxingGlovesFlashing = 0
                    self.node.miniBillboard3Texture = tex
                    t = bs.getGameTime()
                    self.node.miniBillboard3StartTime = t
                    self.node.miniBillboard3EndTime = t+gPowerupWearOffTime
                    self._boxingGlovesWearOffFlashTimer = bs.Timer(gPowerupWearOffTime-2000,bs.WeakCall(self._glovesWearOffFlash))
                    self._boxingGlovesWearOffTimer = bs.Timer(gPowerupWearOffTime,bs.WeakCall(self._glovesWearOff))
            elif m.powerupType == 'speed':
                tex = bs.Powerup.getFactory().texSpeed
                self._flashBillboard(tex)
                self.equipSpeed()
                if bs.getConfig().get('Powerup Popups', True):
                    bsUtils.PopupText((bs.Lstr(resource='speed')),
                                            color=(0.75,1,0.1),
                                            scale=self.scale,
                                            position=self.node.position).autoRetain()
                if self.powerupsExpire:
                    self.node.miniBillboard3Texture = tex
                    t = bs.getGameTime()
                    self.node.miniBillboard3StartTime = t
                    self.node.miniBillboard3EndTime = t+gPowerfulPowerupWearOffTime
                    self._boxingGlovesWearOffFlashTimer = bs.Timer(gPowerfulPowerupWearOffTime-2000,bs.WeakCall(self._speedWearOffFlash))
                    self._boxingGlovesWearOffTimer = bs.Timer(gPowerfulPowerupWearOffTime,bs.WeakCall(self._speedWearOff))
                    
            elif m.powerupType == 'shield':
                player = bs.PlayerSpaz.getPlayer(self)
                self.equipShields(player)
                if bs.getConfig().get('Powerup Popups', True):
                    bsUtils.PopupText((bs.Lstr(resource='shield')),
                                            color=(0.7,0.5,1),
                                            scale=self.scale,
                                            position=self.node.position).autoRetain()
            elif m.powerupType == 'curse':
                self.curse()
                if bs.getConfig().get('Powerup Popups', True):
                    bsUtils.PopupText((bs.Lstr(resource='curse')),
                                            color=(0.3,0,0.45),
                                            scale=self.scale,
                                            position=self.node.position).autoRetain()
            elif (m.powerupType == 'iceBombs'):
                self.bombType = 'ice'
                tex = self._getBombTypeTex()
                self._flashBillboard(tex)
                if bs.getConfig().get('Powerup Popups', True):
                    bsUtils.PopupText((bs.Lstr(resource='iceBomb')),
                                            color=(0,0.45,1.0),
                                            scale=1.0,
                                            position=self.node.position).autoRetain()
                if self.powerupsExpire:
                    self.node.miniBillboard2Texture = tex
                    t = bs.getGameTime()
                    self.node.miniBillboard2StartTime = t
                    self.node.miniBillboard2EndTime = t+gPowerupWearOffTime
                    self._bombWearOffFlashTimer = bs.Timer(gPowerupWearOffTime-2000,bs.WeakCall(self._bombWearOffFlash))
                    self._bombWearOffTimer = bs.Timer(gPowerupWearOffTime,bs.WeakCall(self._bombWearOff))
            elif (m.powerupType == 'fireBombs'):
                self.bombType = 'fire'
                tex = self._getBombTypeTex()
                self._flashBillboard(tex)
                if bs.getConfig().get('Powerup Popups', True):
                    bsUtils.PopupText((bs.Lstr(resource='fireBomb')),
                                            color=(1,0.5,1),
                                            scale=self.scale,
                                            position=self.node.position).autoRetain()
                if self.powerupsExpire:
                    self.node.miniBillboard2Texture = tex
                    t = bs.getGameTime()
                    self.node.miniBillboard2StartTime = t
                    self.node.miniBillboard2EndTime = t+gPowerupWearOffTime
                    self._bombWearOffFlashTimer = bs.Timer(gPowerupWearOffTime-2000,bs.WeakCall(self._bombWearOffFlash))
                    self._bombWearOffTimer = bs.Timer(gPowerupWearOffTime,bs.WeakCall(self._bombWearOff))
            elif (m.powerupType == 'health'):
                if self._cursed:
                    self._cursed = False
                    self.sound.delete() # Stop the curse sound
                    # remove cursed material
                    factory = self.getFactory()
                    for attr in ['materials','rollerMaterials']:
                        materials = getattr(self.node,attr)
                        if factory.curseMaterial in materials:
                            setattr(self.node,attr,tuple(m for m in materials if m != factory.curseMaterial))
                    self.node.curseDeathTime = 0
                if (self.hitPoints > self.hitPointsOverdriveTooMuch):
                    self.hitPoints = self.hitPointsOverdriveTooMuch
                elif (self.hitPoints < self.hitPointsMax):
                    self.hitPoints = self.hitPointsMax
                else:
                    self.hitPoints = self.hitPoints
                self._flashBillboard(bs.Powerup.getFactory().texHealth)
                self.node.hurt = 0
                self._lastHitTime = None
                self._numTimesHit = 0
                if bs.getConfig().get('Powerup Popups', True):
                    bsUtils.PopupText((bs.Lstr(resource='health')),
                                            color=(1,0.9,0.9),
                                            scale=self.scale,
                                            position=self.node.position).autoRetain()
            elif (m.powerupType == 'overdrive'):
                def _safeSetAttr(node,attr,val):
                    if node.exists(): setattr(node,attr,val)
                bs.gameTimer(1,bs.Call(_safeSetAttr,self.node,'invincible',True))
                bs.gameTimer(3000,bs.Call(_safeSetAttr,self.node,'invincible',False))
                if self._cursed:
                    self.curseExplode()
                if (self.hitPoints >= self.hitPointsOverdriveTooMuch):
                    self.curse()
                self.hitPoints = self.hitPoints + self.hitPointsOverdrive
                self._flashBillboard(bs.Powerup.getFactory().texOverdrive)
                self.lightningPower()
                self.node.hurt = 0
                self._lastHitTime = None
                self._numTimesHit = 0
                if bs.getConfig().get('Powerup Popups', True):
                    bsUtils.PopupText((bs.Lstr(resource='overdrive')),
                                            color=(0.5,0,1),
                                            scale=self.scale,
                                            position=self.node.position).autoRetain()
                
            self.node.handleMessage("flash")
            if m.sourceNode.exists():
                m.sourceNode.handleMessage(bs.PowerupAcceptMessage())
            return True

        elif isinstance(m,bs.FreezeMessage):
            if not self.node.exists(): return
            if self.node.invincible == True:
                bs.playSound(self.getFactory().blockSound,1.0,position=self.node.position)
                return
            if self.shield is not None: return
            if not self.frozen:
                if self.healBombCount != 0: # Don't freeze the players that have Healing Bombs in their inventory. Instead of freezing, remove one from the stock.
                    self.setHealBombCount(self.healBombCount-1)
                else:
                    self.frozen = True
                    self.node.frozen = 1
                    bs.gameTimer(5000,bs.WeakCall(self.handleMessage,bs.ThawMessage()))
                    # instantly shatter if we're already dead (otherwise its hard to tell we're dead)
                    if self.hitPoints <= 0:
                        self.shatter()

        elif isinstance(m,bs.ThawMessage):
            if self.frozen and not self.shattered and self.node.exists():
                self.frozen = False
                self.node.frozen = 0
                
        elif isinstance(m,bs.HealMessage):
            factory = self.getFactory()
            if self._cursed:
                self._cursed = False
                self.sound.delete() # Stop the curse sound
                # remove cursed material
                for attr in ['materials','rollerMaterials']:
                    materials = getattr(self.node,attr)
                    if factory.curseMaterial in materials:
                        setattr(self.node,attr,tuple(m for m in materials if m != factory.curseMaterial))
                self.node.curseDeathTime = 0
            if (self.hitPoints <= self.hitPointsMax):
                self.hitPoints = self.hitPointsMax
                bs.playSound(factory.healthPowerupSound,3,position=self.node.position)
            if (self.hitPoints >= self.hitPointsOverdriveTooMuch):
                self.hitPoints = self.hitPointsOverdriveTooMuch
                bs.playSound(factory.healthPowerupSound,3,position=self.node.position)
            if (self.shield is not None): 
                try: player = bs.PlayerSpaz.getPlayer(self)
                except Exception: player = None
                self.equipShields(player)
            bs.gameTimer(1,bs.WeakCall(self.handleMessage,bs.ThawMessage()))
            self.node.hurt = 0
            self._lastHitTime = None
            self._numTimesHit = 0
                
                
        elif isinstance(m,bs.HitMessage):
            if not self.node.exists(): return
            if self.node.invincible == True:
                bs.playSound(self.getFactory().blockSound,1.0,position=self.node.position)
                return True

            # if we were recently hit, don't count this as another
            # (so punch flurries and bomb pileups essentially count as 1 hit)
            gameTime = bs.getGameTime()
            if self._lastHitTime is None or gameTime-self._lastHitTime > 1000:
                self._numTimesHit += 1
                self._lastHitTime = gameTime
            
           
            mag = m.magnitude * self._impactScale
            velocityMag = m.velocityMagnitude * self._impactScale

            damageScale = 0.005 if m.hitSubType == 'knocker' else 0.22 # Knocker deals so much less damage

            # if they've got a shield, deliver it to that instead..
            if self.shield is not None:

                if m.flatDamage: damage = m.flatDamage * self._impactScale
                else:
                    # hit our spaz with an impulse but tell it to only return theoretical damage; not apply the impulse..
                    self.node.handleMessage("impulse",m.pos[0],m.pos[1],m.pos[2],
                                            m.velocity[0],m.velocity[1],m.velocity[2],
                                            mag,velocityMag,m.radius,1,m.forceDirection[0],m.forceDirection[1],m.forceDirection[2])
                    damage = damageScale * self.node.damage

                self.shieldHitPoints -= damage

                self.shield.hurt = 1.0 - self.shieldHitPoints/self.shieldHitPointsMax
                # its a cleaner event if a hit just kills the shield without damaging the player..
                # however, massive damage events should still be able to damage the player..
                # this hopefully gives us a happy medium.
                maxSpillover = 450
                if self.shieldHitPoints <= 0:
                    # fixme - transition out perhaps?..
                    self.shield.delete()
                    self.shield = None
                    bs.playSound(self.getFactory().shieldDownSound,1.0,position=self.node.position)
                    self.shieldSound.delete()
                    # emit some cool lookin sparks when the shield dies
                    t = self.node.position
                    bs.emitBGDynamics(position=(t[0],t[1]+0.9,t[2]),
                                      velocity=self.node.velocity,
                                      count=random.randrange(20,30),scale=0.6,spread=0.6,chunkType='spark')

                else:
                    bs.playSound(self.getFactory().shieldHitSound,0.5,position=self.node.position)

                # emit some cool lookin sparks on shield hit
                bs.emitBGDynamics(position=m.pos,
                                  velocity=(m.forceDirection[0]*1.0,
                                            m.forceDirection[1]*1.0,
                                            m.forceDirection[2]*1.0),
                                  count=min(30,5+int(damage*0.005)),scale=0.3,spread=0.3,chunkType='spark')


                # if they passed our spillover threshold, pass damage along to spaz
                if self.shieldHitPoints <= -maxSpillover:
                    leftoverDamage = -maxSpillover-self.shieldHitPoints
                    shieldLeftoverRatio = leftoverDamage/damage

                    # scale down the magnitudes applied to spaz accordingly..
                    mag *= shieldLeftoverRatio
                    velocityMag *= shieldLeftoverRatio
                else:
                    return True # good job shield!
            else: shieldLeftoverRatio = 1.0

            if m.flatDamage:
                damage = m.flatDamage * self._impactScale * shieldLeftoverRatio
            else:
                # hit it with an impulse and get the resulting damage
                self.node.handleMessage("impulse",m.pos[0],m.pos[1],m.pos[2],
                                        m.velocity[0],m.velocity[1],m.velocity[2],
                                        mag,velocityMag,m.radius,0,m.forceDirection[0],m.forceDirection[1],m.forceDirection[2])

                damage = damageScale * self.node.damage
                

                self.node.handleMessage("hurtSound")

            # play punch impact sound based on damage if it was a punch
            if m.hitType == 'punch':

                self.onPunched(damage)

                # if damage was significant, lets show it
                if damage > 400: bsUtils.showDamageCount('-'+str(int(damage/10))+"%",m.pos,m.forceDirection)
                                               
                # lets always add in a super-punch sound with boxing gloves just to differentiate them
                if m.hitSubType == 'superPunch':
                    bs.playSound(self.getFactory().punchSoundStronger,1.5,
                                 position=self.node.position)
                if damage > 1000:
                    bsUtils.PopupText((bs.Lstr(resource='crit')),
                        color=(1,0,0),
                        scale=1.6,
                        position=self.node.position).autoRetain()
                    self.crit = bs.newNode('light',
                           attrs={'position':self.node.position,
                                  'color': (1,0,0),
                                  'volumeIntensityScale': 1.0}) 
                    bs.animate(self.crit,'intensity',{0:0,250:2.0,750:0},loop=False)
                    bs.gameTimer(750,self.crit.delete)  
                    self.sweat = bs.emitBGDynamics(position=m.pos,
                                  chunkType='sweat',
                                  velocity=(m.forceDirection[0]*1.3,
                                            m.forceDirection[1]*1.3+5.0,
                                            m.forceDirection[2]*1.3),
                                  count=60,
                                  scale=4.0,
                                  spread=0.6);
                    self.sparks = bs.emitBGDynamics(position=m.pos,
                                  chunkType='spark',
                                  velocity=(m.forceDirection[0]*1.3,
                                            m.forceDirection[1]*1.3+5.0,
                                            m.forceDirection[2]*1.3),
                                  count=45,
                                  scale=1.0,
                                  spread=1.0);
                    sounds = self.getFactory().powerPunchSounds
                    sound = sounds[random.randrange(len(sounds))]
                    bs.playSound(sound,2.0,position=self.node.position)
                elif damage > 800:
                    sounds = self.getFactory().punchSoundsStrong
                    sound = sounds[random.randrange(len(sounds))]
                    bs.playSound(sound,1.0,position=self.node.position)
                elif damage > 400:
                    sound = self.getFactory().punchSound   
                    bs.playSound(sound,2.0,position=self.node.position)
                else: 
                    sound = self.getFactory().punchWeakSound
                    bs.playSound(sound,2.0,position=self.node.position)

                # throw up some chunks
                bs.emitBGDynamics(position=m.pos,
                                  velocity=(m.forceDirection[0]*0.5,
                                            m.forceDirection[1]*0.5,
                                            m.forceDirection[2]*0.5),
                                  count=min(10,1+int(damage*0.0025)),scale=0.3,spread=0.03);

                bs.emitBGDynamics(position=m.pos,
                                  chunkType='sweat',
                                  velocity=(m.forceDirection[0]*1.3,
                                            m.forceDirection[1]*1.3+5.0,
                              
              m.forceDirection[2]*1.3),
                                  count=min(30,1+int(damage*0.04)),
                                  scale=1.0,
                                  spread=0.28);
                # momentary flash
                hurtiness = damage*0.003
                punchPos = (m.pos[0]+m.forceDirection[0]*0.02,
                            m.pos[1]+m.forceDirection[1]*0.02,
                            m.pos[2]+m.forceDirection[2]*0.02)
                flashColor = (1.0,0.8,0.4)
                light = bs.newNode("light",
                                   attrs={'position':punchPos,
                                          'radius':0.12+hurtiness*0.12,
                                          'intensity':0.3*(1.0+1.0*hurtiness),
                                          'heightAttenuated':False,
                                          'color':flashColor})
                bs.gameTimer(60,light.delete)


                flash = bs.newNode("flash",
                                   attrs={'position':punchPos,
                                          'size':0.17+0.17*hurtiness,
                                          'color':flashColor})
                bs.gameTimer(60,flash.delete)

            if m.hitType == 'impact':
                bs.emitBGDynamics(position=m.pos,
                                  velocity=(m.forceDirection[0]*2.0,
                                            m.forceDirection[1]*2.0,
                                            m.forceDirection[2]*2.0),
                                  count=min(10,1+int(damage*0.01)),scale=0.4,spread=0.1);
                
            if self.hitPoints > 0:

                # its kinda crappy to die from impacts, so lets reduce impact damage
                # by a reasonable amount if it'll keep us alive
                if m.hitType == 'impact' and damage > self.hitPoints:
                    # drop damage to whatever puts us at 10 hit points, or 200 less than it used to be
                    # whichever is greater (so it *can* still kill us if its high enough)
                    newDamage = max(damage-200,self.hitPoints-10)
                    damage = newDamage

                self.node.handleMessage("flash")
                # if we're holding something, drop it
                if damage > 0.0 and self.node.holdNode.exists():
                    self.node.holdNode = bs.Node(None)
                self.hitPoints -= damage
                self.node.hurt = 1.0 - self.hitPoints/self.hitPointsMax
                # if we're cursed, *any* damage blows us up
                if self._cursed and damage > 0:
                    bs.gameTimer(50,bs.WeakCall(self.curseExplode,m.sourcePlayer))
                # if we're frozen, shatter.. otherwise die if we hit zero
                if self.frozen and (damage > 200 or self.hitPoints <= 0):
                    self.shatter()
                elif self.hitPoints <= 0:
                    self.node.handleMessage(bs.DieMessage(how='impact'))

            # if we're dead, take a look at the smoothed damage val
            # (which gives us a smoothed average of recent damage) and shatter
            # us if its grown high enough
            if self.hitPoints <= 0:
                damageAvg = self.node.damageSmoothed * damageScale
                if damageAvg > 1000:
                    self.shatter()

        elif isinstance(m,_BombDiedMessage):
            self.bombCount += 1
        
        elif isinstance(m,bs.DieMessage):
            # jasonhu5
            if isinstance(self._myBot, SpazBot):
                self._myBot.curseExplode()
            # 

            wasDead = self._dead
            self._dead = True
            self.hitPoints = 0
            if m.immediate:
                self.node.delete()
            elif self.node.exists():
                self.node.hurt = 1.0
                if self.playBigDeathSound and not wasDead:
                    bs.playSound(self.getFactory().singlePlayerDeathSound)
                self.node.dead = True
                bs.gameTimer(2000,self.node.delete)

            # jasonhu5
            self._portal1 = None
            self._portal2 = None
            if self._light1:
                self._light1.delete()
            if self._light2:
                self._light2.delete()
            self._light1 = None
            self._light2 = None
            self._timer = None
            # 

        elif isinstance(m,bs.OutOfBoundsMessage):
            if self._cursed: self.sound.delete() # Stop the curse sound
            self.handleMessage(bs.DieMessage(how='fall'))

        elif isinstance(m,bs.StandMessage):
            self._lastStandPos = (m.position[0],m.position[1],m.position[2])
            self.node.handleMessage("stand",m.position[0],m.position[1],m.position[2],m.angle)

        elif isinstance(m,_CurseExplodeMessage):
            self.curseExplode()

        elif isinstance(m,_PunchHitMessage):
        
            node = bs.getCollisionInfo("opposingNode")

            # only allow one hit per node per punch
            if node is not None and node.exists() and not node in self._punchedNodes:

                punchMomentumAngular = self.node.punchMomentumAngular * self._punchPowerScale
                punchPower = self.node.punchPower * self._punchPowerScale

                # ok here's the deal:  we pass along our base velocity for use in the
                # impulse damage calculations since that is a more predictable value
                # than our fist velocity, which is rather erratic.
                # ...however we want to actually apply force in the direction our fist
                # is moving so it looks better.. so we still pass that along as a direction
                # ..perhaps a time-averased fist-velocity would work too?.. should try that.
                
                # if its something besides another spaz, just do a muffled punch sound
                if node.getNodeType() != 'spaz':
                    if self.node.style == 'cyborg':
                        sounds = self.getFactory().impactMetalSoundsMedium
                    else:
                        sounds = self.getFactory().impactSoundsMedium
                    sound = sounds[random.randrange(len(sounds))]
                    bs.playSound(sound,1.0,position=self.node.position)

                t = self.node.punchPosition
                punchDir = self.node.punchVelocity
                v = self.node.punchMomentumLinear

                self._punchedNodes.add(node)
                node.handleMessage(bs.HitMessage(pos=t,
                                                 velocity=v,
                                                 magnitude=punchPower*punchMomentumAngular*110.0,
                                                 velocityMagnitude=punchPower*40,
                                                 radius=0,
                                                 srcNode=self.node,
                                                 sourcePlayer=self.sourcePlayer,
                                                 forceDirection = punchDir,
                                                 hitType='punch',
                                                 hitSubType='superPunch' if self._hasBoxingGloves else 'default'))

                # also apply opposite to ourself for the first punch only
                # ..this is given as a constant force so that it is more noticable for slower punches
                # where it matters.. for fast awesome looking punches its ok if we punch 'through' the target
                mag = -400.0
                if self._hockey: mag *= 0.5
                if len(self._punchedNodes) == 1:  self.node.handleMessage("kickBack",t[0],t[1],t[2],
                                                                          punchDir[0],punchDir[1],punchDir[2],mag)

        elif isinstance(m,_PickupMessage):
            opposingNode,opposingBody = bs.getCollisionInfo('opposingNode','opposingBody')

            if opposingNode is None or not opposingNode.exists(): return True

            # dont allow picking up of invincible dudes
            try:
                if opposingNode.invincible == True: return True
            except Exception: pass

            # if we're grabbing the pelvis of a non-shattered spaz, we wanna grab the torso instead
            if opposingNode.getNodeType() == 'spaz' and not opposingNode.shattered and opposingBody == 4:
                opposingBody = 1

            # special case - if we're holding a flag, dont replace it
            # ( hmm - should make this customizable or more low level )
            held = self.node.holdNode
            if held is not None and held.exists() and held.getNodeType() == 'flag':
                return True

            self.node.holdBody = opposingBody # needs to be set before holdNode
            self.node.holdNode = opposingNode
        else:
            bs.Actor.handleMessage(self,m)

    def dropBomb(self):
        """
        Tell the spaz to drop one of his bombs, and returns
        the resulting bomb object.
        If the spaz has no bombs or is otherwise unable to
        drop a bomb, returns None.
        """

        if (self.landMineCount <= 0 and self.healBombCount <= 0 and self.grenadeCount <= 0 and self.hijumpCount <= 0 and self.bombCount <= 0) or self.frozen: return
        p = self.node.positionForward
        v = self.node.velocity

        if self.landMineCount > 0:
            droppingBomb = False
            self.setLandMineCount(self.landMineCount-1)
            bombType = 'landMine'
        elif self.healBombCount > 0:
            droppingBomb = False
            self.setHealBombCount(self.healBombCount-1)
            bombType = 'healing'
        elif self.grenadeCount > 0:
            droppingBomb = False
            self.setGrenadeCount(self.grenadeCount-1)
            bombType = 'grenade'
        elif self.hijumpCount > 0:
            droppingBomb = False
            self.setHijumpCount(self.hijumpCount-1)
            bombType = 'hijump'
        else:
            droppingBomb = True
            bombType = self.bombType
            
        if bombType == 'hijump': # Heal the player to compensate for the explosion propelling
            self.hitPoints += 180
            def _jumpSound(node):
                self.node.handleMessage("jumpSound")
            bs.gameTimer(75,bs.Call(_jumpSound,self.node))

        # jasonhu5
        bomb = None
        if bombType == 'overPowerBomb':
            scale = 1.0
            maxOfAll = max(abs(v[0]), abs(v[1]), abs(v[2]))
            offset = 1.0

            # p = self.node.positionForward
            # v = self.node.velocity

            # newPos = p

            # def moveABit(self, v, p):
            #     px = 0.0 + self.node.moveLeftRight * 0.1 + v[0] * 0.1
            #     py = 0.0 - 1.3
            #     pz = 0.0 - self.node.moveUpDown * 0.1 + v[2] * 0.1
            #     return (p[0] + px, p[1] + py, p[2] + pz)
            
            # for i in range(5):
            #     newPos = self.moveABit(v, newPos)
            #     self._player.actor.handleMessage(bs.StandMessage(newPos,random.uniform(0,360)))



            # self._timer = bs.Timer(self.curseTime + 500, bs.Call(gainControlsBack, self))

            speedScale = 3.0
            for i in range(8):
                bomb = bs.Bomb(position=(p[0],p[1] + 2.0,p[2]),
                    velocity=(speedScale * math.sin(math.pi / 4 * i), 0.0, speedScale * math.cos(math.pi / 4 * i)),
                    bombType='impact',
                    blastRadius=self.blastRadius,
                    sourcePlayer=self.sourcePlayer,
                    owner=self.node).autoRetain()

            # # if speed too low, protection bombing
            # if maxOfAll <= 1:

            #     # def gainControlsBack(self):
            #     #     self._player.setActor(self)
            #     #     self.connectControlsToPlayer(self._player)

            #     spaz = SuicideBomber()
            #     spaz.handleMessage(bs.StandMessage((p[0] + 1.0, p[1] + 0.0, p[2]),random.uniform(0,360)))
            #     def _safeSetAttr(node,attr,val):
            #         if node.exists(): setattr(node,attr,val)
            #     bs.gameTimer(1,bs.Call(_safeSetAttr,spaz.node,'hockey',True))
            #     self._player.setActor(spaz)
            #     spaz.connectControlsToPlayer(self._player, self)
            #     self._myBot = spaz

            #     # self._timer = bs.Timer(self.curseTime + 500, bs.Call(gainControlsBack, self))
            #     # speedScale = 4
            #     # for i in range(8):
            #     #     bomb = bs.Bomb(position=(p[0],p[1] + 2.0,p[2]),
            #     #                velocity=(speedScale * math.sin(math.pi / 4 * i), 0.0, speedScale * math.cos(math.pi / 4 * i)),
            #     #                bombType='impact',
            #     #                blastRadius=self.blastRadius,
            #     #                sourcePlayer=self.sourcePlayer,
            #     #                owner=self.node).autoRetain()
            # else:
            #     for i in range(10):
            #         bomb = bs.Bomb(position=(v[0] * offset + p[0] + (scale * i * v[0] / maxOfAll),p[1] + 0.0, v[2] * offset + p[2] + (scale * i * v[2] / maxOfAll)),
            #                        # velocity=(v[0]/maxOfAll*scale ,v[1]/maxOfAll*scale,v[2]/maxOfAll*scale),
            #                        velocity=(v[0],v[1],v[2]),
            #                        bombType=bombType,
            #                        blastRadius=self.blastRadius,
            #                        sourcePlayer=self.sourcePlayer,
            #                        owner=self.node).autoRetain()
        elif bombType == 'grenade':
            portScale = [0.1, 0.1, 0.1]
            offx = -1
            # offz = 1 if v[2] > 0 else -1
            offz = 0
            def shiftSpawnPos(pos):
                return [pos[0] + offx, pos[1], pos[2] + offz]
            # first portal
            if self.grenadeCount == 1:
                bs.screenMessage("first portal")
                self._portal1 = None
                self._portal2 = None
                if self._light1:
                    self._light1.delete()
                if self._light2:
                    self._light2.delete()
                self._light1 = None
                self._light2 = None

                # record position for first gate
                self._teleportal1 = p
                self._light1 = bs.newNode("flash",
                                   attrs={'position':self._teleportal1,
                                          'size':0.17+0.17,
                                          'color': (1.0,0.8,0.4)})
                # bs.gameTimer(60,flash.delete)
                # self._light1 = bs.newNode('light',
                #                            attrs={'position':self._teleportal1,
                #                                   'radius':0.1,
                #                                   'volumeIntensityScale': 10.0})
                
            # second portal
            else:
                bs.screenMessage("second portal")
                self._teleportal2 = p
                self._portal1 = bs.NodeActor(bs.newNode('region',
                                                    attrs={'position':self._teleportal1,
                                                           'scale':portScale,
                                                           'type': 'box',
                                                           'materials':[self._port1Material]}))
                self._portal2 = bs.NodeActor(bs.newNode('region',
                                                    attrs={'position':self._teleportal2,
                                                           'scale':portScale,
                                                           'type': 'box',
                                                           'materials':[self._port2Material]}))
                self._light2 = bs.newNode('light',
                                           attrs={'position':self._teleportal2,
                                                  'radius': 0.1,
                                                  'volumeIntensityScale': 10.0})

                self._teleportal1 = shiftSpawnPos(self._teleportal1)
                self._teleportal2 = shiftSpawnPos(self._teleportal2)
        else:
            bomb = bs.Bomb(position=(p[0],p[1] - 0.0,p[2]),
                           velocity=(v[0],v[1],v[2]),
                           bombType=bombType,
                           blastRadius=self.blastRadius,
                           sourcePlayer=self.sourcePlayer,
                           owner=self.node).autoRetain()

        # bomb = bs.Bomb(position=(p[0],p[1] - 0.0,p[2]),
        #                    velocity=(v[0],v[1],v[2]),
        #                    bombType=bombType,
        #                    blastRadius=self.blastRadius,
        #                    sourcePlayer=self.sourcePlayer,
        #                    owner=self.node).autoRetain()

        # jasonhu5
        if not bombType == 'overPowerBomb' and not bombType == 'grenade':
            if droppingBomb:
                self.bombCount -= 1
                bomb.node.addDeathAction(bs.WeakCall(self.handleMessage,_BombDiedMessage()))

            self._pickUp(bomb.node)
        # if droppingBomb:
        #     self.bombCount -= 1
        #     bomb.node.addDeathAction(bs.WeakCall(self.handleMessage,_BombDiedMessage()))

        # self._pickUp(bomb.node)

        for c in self._droppedBombCallbacks: c(self,bomb)
        
        return bomb

    def _pickUp(self,node):
        if self.node.exists() and node.exists():
            self.node.holdBody = 0 # needs to be set before holdNode
            self.node.holdNode = node
            
    def setGrenadeCount(self,count):
        """
        Set the number of grenades this spaz is carrying.
        """
        self.grenadeCount = count
        if self.node.exists():
            if self.grenadeCount != 0:
                self.node.counterText = 'x'+str(self.grenadeCount)
                self.node.counterTexture = bs.Powerup.getFactory().texGrenades
            else:
                self.node.counterText = ''
                
    def setHijumpCount(self,count):
        """
        Set the number of hi-jumps this spaz has.
        """
        self.hijumpCount = count
        if self.node.exists():
            if self.hijumpCount != 0:
                self.node.counterText = 'x'+str(self.hijumpCount)
                self.node.counterTexture = bs.Powerup.getFactory().texHijump
            else:
                self.node.counterText = ''
        
    def setLandMineCount(self,count):
        """
        Set the number of land-mines this spaz is carrying.
        """
        self.landMineCount = count
        if self.node.exists():
            if self.landMineCount != 0:
                self.node.counterText = 'x'+str(self.landMineCount)
                self.node.counterTexture = bs.Powerup.getFactory().texLandMines
            else:
                self.node.counterText = ''
                
    def setHealBombCount(self,count):
        """
        Set the number of tesla plates this spaz is carrying.
        """
        self.healBombCount = count
        if self.node.exists():
            if self.healBombCount != 0:
                self.node.counterText = 'x'+str(self.healBombCount)
                self.node.counterTexture = bs.Powerup.getFactory().texHealBombs
            else:
                self.node.counterText = ''

    def bombOnHead(self):
        p = self.node.positionForward
        # v = self.node.velocity
        # print("hello")
        # print(p)
        # print(v)
        bomb = bs.Bomb(position=(p[0],p[1] + 2.5,p[2]),
                       velocity=(0,0,0),
                       bombType='impact',
                       blastRadius=self.blastRadius,
                       sourcePlayer=self.sourcePlayer,
                       owner=self.node).autoRetain()

    def unarmCurse(self):
        self.curseExplodeTimer = None

    def curseExplode(self,sourcePlayer=None):
        """
        Explode the poor spaz as happens when
        a curse timer runs out.
        """

        # convert None to an empty player-ref

        # jasonhu5
        # if sourcePlayer is None: sourcePlayer = bs.Player(None)
        
        # fallTimeInterval = 200
        # totalCurseTime = 5000

        # self.curseExplodeTimer = bs.Timer(fallTimeInterval,bs.WeakCall(self.bombOnHead), repeat=True)
        # self._timer = bs.Timer(totalCurseTime, bs.WeakCall(self.unarmCurse))

        # # tmr = bs.Timer(1000,bs.Call(bs.screenMessage, "H"),repeat=True)
        # # self.curseExplodeTimer = bs.Timer(self.curseTime,bs.Call(bs.screenMessage, "XHE"))

        # if self._cursed and self.node.exists():
        #     self.sound.delete() # Stop the curse sound
        #     # for i in range(5):
        #         # print("x")
        #     self.curseExplodeTimer = bs.Timer(fallTimeInterval,bs.WeakCall(self.bombOnHead), repeat=True)
        #     self._timer = bs.Timer(totalCurseTime, bs.WeakCall(self.unarmCurse))

        #     self._cursed = False
        #        

        if sourcePlayer is None: sourcePlayer = bs.Player(None)
        
        if self._cursed and self.node.exists():
            self.sound.delete() # Stop the curse sound
            self.shatter(extreme=True)
            activity = self._activity()
            if activity:
                bs.Blast(position=self.node.position,
                    velocity=self.node.velocity,
                    blastRadius=4.0 if not isinstance(bs.getSession(),bs.CoopSession) else 2.0,blastType='normal',
                    sourcePlayer=sourcePlayer if sourcePlayer.exists() else self.sourcePlayer).autoRetain()
            self.handleMessage(bs.DieMessage())
            self._cursed = False

    def shatter(self,extreme=False):
        """
        Break the poor spaz into little bits.
        """
        if self.shattered: return
        self.shattered = True
        if self.frozen:
            # momentary flash of light
            light = bs.newNode('light',
                               attrs={'position':self.node.position,
                                      'radius':0.5,
                                      'heightAttenuated':False,
                                      'color': (0.8,0.8,1.0)})
            
            bs.animate(light,'intensity',{0:3.0, 40:0.5, 80:0.07, 300:0})
            bs.gameTimer(300,light.delete)
            # emit ice chunks..
            bs.emitBGDynamics(position=self.node.position,
                              velocity=self.node.velocity,
                              count=int(random.random()*10.0+10.0),scale=0.6,spread=0.2,chunkType='ice');
            bs.emitBGDynamics(position=self.node.position,
                              velocity=self.node.velocity,
                              count=int(random.random()*10.0+10.0),scale=0.3,spread=0.2,chunkType='ice');

            bs.playSound(self.getFactory().shatterSound,1.0,position=self.node.position)
        else:
            bs.playSound(self.getFactory().splatterSound,1.0,position=self.node.position)
        self.handleMessage(bs.DieMessage())
        self.node.shattered = 2 if extreme else 1

    def _hitSelf(self,intensity):

        # clean exit if we're dead..
        try: pos = self.node.position
        except Exception: return

        self.handleMessage(bs.HitMessage(flatDamage=50.0*intensity,
                                         pos=pos,
                                         forceDirection=self.node.velocity,
                                         hitType='impact'))
        self.node.handleMessage("knockout",max(0.0,50.0*intensity))
        if intensity > 5: 
            if self.node.style == 'cyborg':
                sounds = self.getFactory().impactMetalSoundsHarder
            else:
                sounds = self.getFactory().impactSoundsHarder
        elif intensity > 2: 
            if self.node.style == 'cyborg':
                sounds = self.getFactory().impactMetalSoundsHard
            else:
                sounds = self.getFactory().impactSoundsHard
        else: 
            if self.node.style == 'cyborg':
                sounds = self.getFactory().impactMetalSoundsMedium
            else:
                sounds = self.getFactory().impactSoundsMedium
        s = sounds[random.randrange(len(sounds))]
        bs.playSound(s,position=pos,volume=4)
        
    def _getBombTypeTex(self):
        bombFactory = bs.Powerup.getFactory()
        if self.bombType == 'sticky': return bombFactory.texStickyBombs
        # jasonhu5
        elif self.bombType == 'overPowerBomb': return bombFactory.texStickyBombs
        # 
        elif self.bombType == 'ice': return bombFactory.texIceBombs
        elif self.bombType == 'fire': return bombFactory.texFireBombs
        elif self.bombType == 'ranger': return bombFactory.texRangerBombs
        elif self.bombType == 'combat': return bombFactory.texCombatBombs
        elif self.bombType == 'knocker': return bombFactory.texKnockerBombs
        elif self.bombType == 'dynamite': return bombFactory.texDynamitePack
        elif self.bombType == 'impact': return bombFactory.texImpactBombs
        elif self.bombType == 'healing': return bombFactory.texHealBombs
        elif self.bombType == 'hijump': return bombFactory.texHijump
        elif self.bombType == 'speed': return bombFactory.texSpeed
        else: raise Exception()
        
    def _flashBillboard(self,tex):
        self.node.billboardTexture = tex
        self.node.billboardCrossOut = False
        bs.animate(self.node,"billboardOpacity",{0:0.0,250:1.0,500:0.0})

    def setBombCount(self,count):
        # we cant just set bombCount cuz some bombs may be laid currently
        # so we have to do a relative diff based on max
        diff = count - self._maxBombCount
        self._maxBombCount += diff
        self.bombCount += diff
        
    def _speedWearOffFlash(self):
        if self.node.exists():
            self.node.billboardTexture = bs.Powerup.getFactory().texSpeed
            self.node.billboardOpacity = 1.0
            self.node.billboardCrossOut = True

    def _speedWearOff(self):
        factory = self.getFactory()
        if self._hasBoxingGloves:
            self._punchPowerScale = gBasePunchPowerScale
            self._punchCooldown = gBasePunchCooldown
        def _safeSetAttr(node,attr,val):
                if node.exists(): setattr(node,attr,val)
        bs.gameTimer(1,bs.Call(_safeSetAttr,self.node,'hockey',False))
        if self.node.exists():
            bs.playSound(bs.Powerup.getFactory().powerdownSound,position=self.node.position)
            bs.playSound(factory.speedDownSound,position=self.node.position)
            self.node.billboardOpacity = 0.0

    def _glovesWearOffFlash(self):
        if self.node.exists():
            self.node.boxingGlovesFlashing = 1
            self.node.billboardTexture = bs.Powerup.getFactory().texPunch
            self.node.billboardOpacity = 1.0
            self.node.billboardCrossOut = True

    def _glovesWearOff(self):
        self._punchPowerScale = gBasePunchPowerScale
        self._punchCooldown = gBasePunchCooldown
        self._hasBoxingGloves = False
        if self.node.exists():
            bs.playSound(bs.Powerup.getFactory().powerdownSound,position=self.node.position)
            self.node.boxingGloves = 0
            self.node.billboardOpacity = 0.0
            
    def _blastBuffWearOffFlash(self):
        if self.node.exists():
            self.node.billboardTexture = bs.Powerup.getFactory().texBlast
            self.node.billboardOpacity = 1.0
            self.node.billboardCrossOut = True

    def _blastBuffWearOff(self):
        self.setBombCount(self.defaultBombCount)
        self.blastRadius = self.defaultBlastRadius
        if self.node.exists():
            bs.playSound(bs.Powerup.getFactory().powerdownSound,position=self.node.position)
            self.node.billboardOpacity = 0.0

    def _multiBombWearOffFlash(self):
        if self.node.exists():
            self.node.billboardTexture = bs.Powerup.getFactory().texBomb
            self.node.billboardOpacity = 1.0
            self.node.billboardCrossOut = True

    def _multiBombWearOff(self):
        self.setBombCount(self.defaultBombCount)
        if self.node.exists():
            bs.playSound(bs.Powerup.getFactory().powerdownSound,position=self.node.position)
            self.node.billboardOpacity = 0.0

    def _bombWearOffFlash(self):
        if self.node.exists():
            self.node.billboardTexture = self._getBombTypeTex()
            self.node.billboardOpacity = 1.0
            self.node.billboardCrossOut = True

    def _bombWearOff(self):
        self.bombType = self.bombTypeDefault
        if self.node.exists():
            bs.playSound(bs.Powerup.getFactory().powerdownSound,position=self.node.position)
            self.node.billboardOpacity = 0.0

class PlayerSpazDeathMessage(object):
    """
    category: Message Classes

    A bs.PlayerSpaz has died.

    Attributes:

       spaz
          The bs.PlayerSpaz that died.

       killed
          If True, the spaz was killed;
          If False, they left the game or the round ended.

       killerPlayer
          The bs.Player that did the killing, or None.

       how
          The particular type of death.
    """
    def __init__(self,spaz,wasKilled,killerPlayer,how):
        """
        Instantiate a message with the given values.
        """
        self.spaz = spaz
        self.killed = wasKilled
        self.killerPlayer = killerPlayer
        self.how = how

class PlayerSpazHurtMessage(object):
    """
    category: Message Classes

    A bs.PlayerSpaz was hurt.

    Attributes:

       spaz
          The bs.PlayerSpaz that was hurt
    """
    def __init__(self,spaz):
        """
        Instantiate with the given bs.Spaz value.
        """
        self.spaz = spaz


class PlayerSpaz(Spaz):
    """
    category: Game Flow Classes
    
    A bs.Spaz subclass meant to be controlled by a bs.Player.

    When a PlayerSpaz dies, it delivers a bs.PlayerSpazDeathMessage
    to the current bs.Activity. (unless the death was the result of the
    player leaving the game, in which case no message is sent)

    When a PlayerSpaz is hurt, it delivers a bs.PlayerSpazHurtMessage
    to the current bs.Activity.
    """


    def __init__(self,color=(1,1,1),highlight=(0.5,0.5,0.5),character="Spaz",player=None,powerupsExpire=True):
        """
        Create a spaz for the provided bs.Player.
        Note: this does not wire up any controls;
        you must call connectControlsToPlayer() to do so.
        """
        # convert None to an empty player-ref
        if player is None: player = bs.Player(None)
        
        Spaz.__init__(self,color=color,highlight=highlight,character=character,sourcePlayer=player,startInvincible=True,powerupsExpire=powerupsExpire)
        self.lastPlayerAttackedBy = None # FIXME - should use empty player ref
        self.lastAttackedTime = 0
        self.lastAttackedType = None
        self.heldCount = 0
        self.lastPlayerHeldBy = None # FIXME - should use empty player ref here
        self._player = player

        # grab the node for this player and wire it to follow our spaz (so players' controllers know where to draw their guides, etc)
        if player.exists():
            playerNode = bs.getActivity()._getPlayerNode(player)
            self.node.connectAttr('torsoPosition',playerNode,'position')

    def __superHandleMessage(self,m):
        super(PlayerSpaz,self).handleMessage(m)
        
    def getPlayer(self):
        """
        Return the bs.Player associated with this spaz.
        Note that while a valid player object will always be
        returned, there is no guarantee that the player is still
        in the game.  Call bs.Player.exists() on the return value
        before doing anything with it.
        """
        return self._player

    def connectControlsToPlayer(self,enableJump=True,enablePunch=True,enablePickUp=True,enableBomb=True,enableRun=True,enableFly=True):
        """
        Wire this spaz up to the provided bs.Player.
        Full control of the character is given by default
        but can be selectively limited by passing False
        to specific arguments.
        """

        player = self.getPlayer()
        
        # reset any currently connected player and/or the player we're now wiring up
        if self._connectedToPlayer is not None:
            if player != self._connectedToPlayer: player.resetInput()
            self.disconnectControlsFromPlayer()
        else: player.resetInput()

        player.assignInputCall('upDown',self.onMoveUpDown)
        player.assignInputCall('leftRight',self.onMoveLeftRight)
        player.assignInputCall('holdPositionPress',self._onHoldPositionPress)
        player.assignInputCall('holdPositionRelease',self._onHoldPositionRelease)

        if enableJump:
            player.assignInputCall('jumpPress',self.onJumpPress)
            player.assignInputCall('jumpRelease',self.onJumpRelease)
        if enablePickUp:
            player.assignInputCall('pickUpPress',self.onPickUpPress)
            player.assignInputCall('pickUpRelease',self.onPickUpRelease)
        if enablePunch:
            player.assignInputCall('punchPress',self.onPunchPress)
            player.assignInputCall('punchRelease',self.onPunchRelease)
        if enableBomb:
            player.assignInputCall('bombPress',self.onBombPress)
            player.assignInputCall('bombRelease',self.onBombRelease)
        if enableRun:
            player.assignInputCall('run',self.onRun)
        if enableFly:
            player.assignInputCall('flyPress',self.onFlyPress)
            player.assignInputCall('flyRelease',self.onFlyRelease)

        self._connectedToPlayer = player

        
    def disconnectControlsFromPlayer(self):
        """
        Completely sever any previously connected
        bs.Player from control of this spaz.
        """
        if self._connectedToPlayer is not None:
            self._connectedToPlayer.resetInput()
            self._connectedToPlayer = None
            # send releases for anything in case its held..
            self.onMoveUpDown(0)
            self.onMoveLeftRight(0)
            self._onHoldPositionRelease()
            self.onJumpRelease()
            self.onPickUpRelease()
            self.onPunchRelease()
            self.onBombRelease()
            self.onRun(0.0)
            self.onFlyRelease()
        else: print 'WARNING: disconnectControlsFromPlayer() called for non-connected player'


    def handleMessage(self,m):
        self._handleMessageSanityCheck()

        # keep track of if we're being held and by who most recently
        if isinstance(m,bs.PickedUpMessage):
            self.__superHandleMessage(m) # augment standard behavior
            self.heldCount += 1
            pickedUpBy = m.node.sourcePlayer
            if pickedUpBy is not None and pickedUpBy.exists():
                self.lastPlayerHeldBy = pickedUpBy

        elif isinstance(m,bs.DroppedMessage):
            self.__superHandleMessage(m) # augment standard behavior
            self.heldCount -= 1
            if self.heldCount < 0:
                print "ERROR: spaz heldCount < 0"
            # let's count someone dropping us as an attack..
            try: pickedUpBy = m.node.sourcePlayer
            except Exception: pickedUpBy = None
            if pickedUpBy is not None and pickedUpBy.exists():
                self.lastPlayerAttackedBy = pickedUpBy
                self.lastAttackedTime = bs.getGameTime()
                self.lastAttackedType = ('pickedUp','default')
            
        elif isinstance(m,bs.DieMessage):

            # report player deaths to the game
            if not self._dead:

                # immediate-mode or left-game deaths don't count as 'kills'
                killed = (m.immediate==False and m.how!='leftGame')

                activity = self._activity()

                if not killed:
                    killerPlayer = None
                else:
                    # if this player was being held at the time of death, the holder is the killer
                    if self.heldCount > 0 and self.lastPlayerHeldBy is not None and self.lastPlayerHeldBy.exists():
                        killerPlayer = self.lastPlayerHeldBy
                    else:
                        # otherwise, if they were attacked by someone in the last few seconds,
                        # that person's the killer.. otherwise it was a suicide.
                        # FIXME - currently disabling suicides in Co-Op since all bot kills would
                        # register as suicides; need to change this from lastPlayerAttackedBy to
                        # something like lastActorAttackedBy to fix that.
                        if self.lastPlayerAttackedBy is not None and self.lastPlayerAttackedBy.exists() and bs.getGameTime() - self.lastAttackedTime < 4000:
                            killerPlayer = self.lastPlayerAttackedBy
                        else:
                            # ok, call it a suicide unless we're in co-op
                            if activity is not None and not isinstance(activity.getSession(), bs.CoopSession):
                                killerPlayer = self.getPlayer()
                            else:
                                killerPlayer = None
                            
                if killerPlayer is not None and not killerPlayer.exists():
                    killerPlayer = None

                # only report if both the player and the activity still exist
                if killed and activity is not None and self.getPlayer().exists():
                    activity.handleMessage(PlayerSpazDeathMessage(self, killed, killerPlayer, m.how))
                    
            self.__superHandleMessage(m) # augment standard behavior

        # keep track of the player who last hit us for point rewarding
        elif isinstance(m,bs.HitMessage):
            if m.sourcePlayer is not None and m.sourcePlayer.exists():
                self.lastPlayerAttackedBy = m.sourcePlayer
                self.lastAttackedTime = bs.getGameTime()
                self.lastAttackedType = (m.hitType,m.hitSubType)
            self.__superHandleMessage(m) # augment standard behavior
            activity = self._activity()
            if activity is not None:
                activity.handleMessage(PlayerSpazHurtMessage(self))
        else:
            Spaz.handleMessage(self,m)


class RespawnIcon(object):
    """
    category: Game Flow Classes

    An icon with a countdown that appears alongside the screen;
    used to indicate that a bs.Player is waiting to respawn.
    """
    
    def __init__(self,player,respawnTime):
        """
        Instantiate with a given bs.Player and respawnTime (in milliseconds)
        """
        activity = bs.getActivity()
        onRight = False
        self._visible = True
        if isinstance(bs.getSession(),bs.TeamsSession):
            onRight = player.getTeam().getID()%2==1
            # store a list of icons in the team
            try: respawnIcons = player.getTeam().gameData['_spazRespawnIconsRight']
            except Exception: respawnIcons = player.getTeam().gameData['_spazRespawnIconsRight'] = {}
            offsExtra = -20
        else:
            onRight = False
            # store a list of icons in the activity
            try: respawnIcons = activity._spazRespawnIconsRight
            except Exception: respawnIcons = activity._spazRespawnIconsRight = {}
            if isinstance(activity.getSession(),bs.FreeForAllSession): offsExtra = -150
            else: offsExtra = -20

        try: maskTex = player.getTeam().gameData['_spazRespawnIconsMaskTex']
        except Exception: maskTex = player.getTeam().gameData['_spazRespawnIconsMaskTex'] = bs.getTexture('characterIconMask')

        # now find the first unused slot and use that
        index = 0
        while index in respawnIcons and respawnIcons[index]() is not None and respawnIcons[index]()._visible: index += 1
        respawnIcons[index] = weakref.ref(self)

        offs = offsExtra + index*-53
        icon = player.getIcon()
        texture = icon['texture']
        hOffs = -10
        self._image = bs.NodeActor(bs.newNode('image',
                                              attrs={'texture':texture,
                                                     'tintTexture':icon['tintTexture'],
                                                     'tintColor':icon['tintColor'],
                                                     'tint2Color':icon['tint2Color'],
                                                     'maskTexture':maskTex,
                                                     'position':(-40-hOffs if onRight else 40+hOffs,-180+offs),
                                                     'scale':(32,32),
                                                     'opacity':1.0,
                                                     'absoluteScale':True,
                                                     'attach':'topRight' if onRight else 'topLeft'}))
        
        bs.animate(self._image.node,'opacity',{0:0,200:0.7})

        self._name = bs.NodeActor(bs.newNode('text',
                                             attrs={'vAttach':'top',
                                                    'hAttach':'right' if onRight else 'left',
                                                    'text':player.getName(),
                                                    'maxWidth':100,
                                                    'hAlign':'center',
                                                    'vAlign':'center',
                                                    'shadow':1.0,
                                                    'flatness':1.0,
                                                    'color':bs.getSafeColor(icon['tintColor']),
                                                    'scale':0.5,
                                                    'position':(-40-hOffs if onRight else 40+hOffs,-205+49+offs)}))
        
        bs.animate(self._name.node,'scale',{0:0,100:0.5})

        self._text = bs.NodeActor(bs.newNode('text',
                                             attrs={'position':(-60-hOffs if onRight else 60+hOffs,-192+offs),
                                                    'hAttach':'right' if onRight else 'left',
                                                    'hAlign':'right' if onRight else 'left',
                                                    'scale':0.9,
                                                    'shadow':0.5,
                                                    'flatness':0.5,
                                                    'vAttach':'top',
                                                    'color':bs.getSafeColor(icon['tintColor']),
                                                    'text':''}))
        
        bs.animate(self._text.node,'scale',{0:0,100:0.9})

        self._respawnTime = bs.getGameTime()+respawnTime
        self._update()
        self._timer = bs.Timer(1000,bs.WeakCall(self._update),repeat=True)

    def _update(self):
        remaining = int(round(self._respawnTime-bs.getGameTime())/1000.0)
        if remaining > 0:
            if self._text.node.exists():
                self._text.node.text = str(remaining)
        else: self._clear()
            
    def _clear(self):
        self._visible = False
        self._image = self._text = self._timer = self._name = None
        


class SpazBotPunchedMessage(object):
    """
    category: Message Classes


    A bs.SpazBot got punched.

    Attributes:

       badGuy
          The bs.SpazBot that got punched.

       damage
          How much damage was done to the bs.SpazBot.
    """
    def __init__(self,badGuy,damage):
        """
        Instantiate a message with the given values.
        """

        self.badGuy = badGuy
        self.damage = damage

class SpazBotDeathMessage(object):
    """
    category: Message Classes


    A bs.SpazBot has died.

    Attributes:

       badGuy
          The bs.SpazBot that was killed.

       killerPlayer
          The bs.Player that killed it (or None).

       how
          The particular type of death.
    """
    def __init__(self,badGuy,killerPlayer,how):
        """
        Instantiate with given values.
        """
        self.badGuy = badGuy
        self.killerPlayer = killerPlayer
        self.how = how

        
class SpazBot(Spaz):
    """
    category: Bot Classes

    A really dumb AI version of bs.Spaz.
    Add these to a bs.BotSet to use them.

    Note: currently the AI has no real ability to
    navigate obstacles and so should only be used
    on wide-open maps.

    When a SpazBot is killed, it delivers a bs.SpazBotDeathMessage
    to the current activity.

    When a SpazBot is punched, it delivers a bs.SpazBotPunchedMessage
    to the current activity.
    """

    # jasonhu5
    isBotFriendly = False
    _player = None
    _ownerPlayerSpaz = None
    # 

    character = 'Spaz'
    punchiness = 0.5
    throwiness = 0.7
    static = False
    bouncy = False
    run = False
    chargeDistMin = 0.0 # when we can start a new charge
    chargeDistMax = 2.0 # when we can start a new charge
    runDistMin = 0.0 # how close we can be to continue running
    chargeSpeedMin = 0.4
    chargeSpeedMax = 1.0
    throwDistMin = 5.0
    throwDistMax = 9.0
    throwRate = 1.0
    defaultBombType = 'normal'
    defaultBombCount = 3
    startCursed = False
    color=gDefaultBotColor
    highlight=gDefaultBotHighlight

    # jasonhu5
    def getPlayer(self):
        return self._player
        
    def connectControlsToPlayer(self,player,spaz,enableJump=True,enablePunch=True,enablePickUp=True,enableBomb=True,enableRun=True,enableFly=True):
        """
        Wire this spaz up to the provided bs.Player.
        Full control of the character is given by default
        but can be selectively limited by passing False
        to specific arguments.
        """
        
        player.resetInput()
        self._player = player
        self._ownerPlayerSpaz = spaz

        # reset any currently connected player and/or the player we're now wiring up
        # if self._connectedToPlayer is not None:
        #     if player != self._connectedToPlayer: player.resetInput()
        #     self.disconnectControlsFromPlayer()
        # else: player.resetInput()

        player.assignInputCall('upDown',self.onMoveUpDown)
        player.assignInputCall('leftRight',self.onMoveLeftRight)
        player.assignInputCall('holdPositionPress',self._onHoldPositionPress)
        player.assignInputCall('holdPositionRelease',self._onHoldPositionRelease)

        if enableJump:
            player.assignInputCall('jumpPress',self.onJumpPress)
            player.assignInputCall('jumpRelease',self.onJumpRelease)
        if enablePickUp:
            player.assignInputCall('pickUpPress',self.onPickUpPress)
            player.assignInputCall('pickUpRelease',self.onPickUpRelease)
        if enablePunch:
            player.assignInputCall('punchPress',self.onPunchPress)
            player.assignInputCall('punchRelease',self.onPunchRelease)
        if enableBomb:
            player.assignInputCall('bombPress',self.onBombPress)
            player.assignInputCall('bombRelease',self.onBombRelease)
        if enableRun:
            player.assignInputCall('run',self.onRun)
        if enableFly:
            player.assignInputCall('flyPress',self.onFlyPress)
            player.assignInputCall('flyRelease',self.onFlyRelease)

        # self._connectedToPlayer = player
    # 

    def __init__(self):
        """
        Instantiate a spaz-bot.
        """
        Spaz.__init__(self,color=self.color,highlight=self.highlight,character=self.character,
                      sourcePlayer=None,startInvincible=False,canAcceptPowerups=False)

        # if you need to add custom behavior to a bot, set this to a callable which takes one
        # arg (the bot) and returns False if the bot's normal update should be run and True if not
        self.updateCallback = None
        self._map = weakref.ref(bs.getActivity().getMap())

        self.lastPlayerAttackedBy = None # FIXME - should use empty player-refs
        self.lastAttackedTime = 0
        self.lastAttackedType = None
        self.targetPointDefault = None
        self.heldCount = 0
        self.lastPlayerHeldBy = None # FIXME - should use empty player-refs here
        self.targetFlag = None
        self._chargeSpeed = 0.5*(self.chargeSpeedMin+self.chargeSpeedMax)
        self._leadAmount = 0.5
        self._mode = 'wait'
        self._chargeClosingIn = False
        self._lastChargeDist = 0.0
        self._running = False
        self._lastJumpTime = 0

        if self.startCursed: self.curse()
            
    def _getTargetPlayerPt(self):
        """ returns the default player pt we're targeting """
        bp = bs.Vector(*self.node.position)
        closestLen = None
        closestVel = None
        for pp,pv in self._playerPts:

            l = (pp-bp).length()
            # ignore player-points that are significantly below the bot
            # (keeps bots from following players off cliffs)
            if (closestLen is None or l < closestLen) and (pp[1] > bp[1] - 5.0):
                closestLen = l
                closestVel = pv
                closest = pp
        if closestLen is not None:
            return (bs.Vector(closest[0],closest[1],closest[2]),
                    bs.Vector(closestVel[0],closestVel[1],closestVel[2]))
        else:
            return None,None

    def _setPlayerPts(self,pts):
        """
        Provide the spaz-bot with the locations of players.
        """
        self._playerPts = pts

    def _updateAI(self):
        """
        Should be called periodically to update the spaz' AI
        """

        # jasonhu5
        if self.isBotFriendly:
            if self.run:
                self._leadAmount = 0.3
                self._running = True
                self.node.run = 1.0
            else:
                self._leadAmont = 0.01
                self._running = False
                self.node.run = 0.0

            return
        # 
        
        if self.updateCallback is not None:
            if self.updateCallback(self) == True:
                return # true means bot has been handled

        t = self.node.position
        ourPos = bs.Vector(t[0],0,t[2])
        canAttack = True

        # if we're a flag-bearer, we're pretty simple-minded - just walk towards the flag and try to pick it up
        if self.targetFlag is not None:

            if not self.targetFlag.node.exists():
                # our flag musta died :-C
                self.targetFlag = None
                return
            if self.node.holdNode.exists():
                try: holdingFlag = (self.node.holdNode.getNodeType() == 'flag')
                except Exception: holdingFlag = False
            else: holdingFlag = False
            # if we're holding the flag, just walk left
            if holdingFlag:
                # just walk left
                self.node.moveLeftRight = -1.0
                self.node.moveUpDown = 0.0
            # otherwise try to go pick it up
            else:
                targetPtRaw = bs.Vector(*self.targetFlag.node.position)
                targetVel = bs.Vector(0,0,0)
                diff = (targetPtRaw-ourPos)
                diff = bs.Vector(diff[0],0,diff[2]) # dont care about y
                dist = diff.length()
                toTarget = diff.normal()

                # if we're holding some non-flag item, drop it
                if self.node.holdNode.exists():
                    self.node.pickUpPressed = True
                    self.node.pickUpPressed = False
                    return

                # if we're a runner, run only when not super-near the flag
                if self.run and dist > 3.0:
                    self._running = True
                    self.node.run = 1.0
                else:
                    self._running = False
                    self.node.run = 0.0

                self.node.moveLeftRight = toTarget.x()
                self.node.moveUpDown = -toTarget.z()
                if dist < 1.25:
                    self.node.pickUpPressed = True
                    self.node.pickUpPressed = False
            return
        # not a flag-bearer.. if we're holding anything but a bomb, drop it
        else:
            if self.node.holdNode.exists():
                try: holdingBomb = (self.node.holdNode.getNodeType() in ['bomb','prop'])
                except Exception: holdingBomb = False
                if not holdingBomb:
                    self.node.pickUpPressed = True
                    self.node.pickUpPressed = False
                    return
            
        targetPtRaw,targetVel = self._getTargetPlayerPt()

        if targetPtRaw is None:
            # use default target if we've got one
            if self.targetPointDefault is not None:
                targetPtRaw = self.targetPointDefault
                targetVel = bs.Vector(0,0,0)
                canAttack = False
            # with no target, we stop moving and drop whatever we're holding
            else:
                self.node.moveLeftRight = 0
                self.node.moveUpDown = 0
                if self.node.holdNode.exists():
                    self.node.pickUpPressed = True
                    self.node.pickUpPressed = False
                return

        # we dont want height to come into play
        targetPtRaw.data[1] = 0
        targetVel.data[1] = 0

        distRaw = (targetPtRaw-ourPos).length()
        # use a point out in front of them as real target (more out in front the farther from us they are)
        targetPt = targetPtRaw + targetVel*distRaw*0.3*self._leadAmount

        diff = (targetPt-ourPos)
        dist = diff.length()
        toTarget = diff.normal()

        if self._mode == 'throw':
            # we can only throw if alive and well..
            if not self._dead and not self.node.knockout:

                timeTillThrow = self._throwReleaseTime-bs.getGameTime()

                if not self.node.holdNode.exists():
                    # if we havnt thrown yet, whip out the bomb
                    if not self._haveDroppedThrowBomb:
                        self.dropBomb()
                        self._haveDroppedThrowBomb = True
                    # otherwise our lack of held node means we successfully released our bomb.. lets retreat now
                    else:
                        self._mode = 'flee'

                # oh crap we're holding a bomb.. better throw it.
                elif timeTillThrow <= 0:
                    # jump and throw..
                    def _safePickup(node):
                        if node.exists():
                            self.node.pickUpPressed = True
                            self.node.pickUpPressed = False
                    if dist > 5.0:
                        self.node.jumpPressed = True
                        self.node.jumpPressed = False
                        bs.gameTimer(100,bs.Call(_safePickup,self.node)) # throws
                    else:
                        bs.gameTimer(1,bs.Call(_safePickup,self.node)) # throws

                if self.static:
                    if timeTillThrow < 300: speed = 1.0
                    elif timeTillThrow < 700 and dist > 3.0: speed = -1.0 # whiplash for long throws
                    else: speed = 0.02
                else:
                    if timeTillThrow < 700:
                        # right before throw charge full speed towards target
                        speed = 1.0
                    else:
                        # earlier we can hold or move backward for a whiplash
                        speed = 0.0125
                self.node.moveLeftRight = toTarget.x() * speed
                self.node.moveUpDown = toTarget.z() * -1.0 * speed

        elif self._mode == 'charge':
            if random.random() < 0.3:
                self._chargeSpeed = random.uniform(self.chargeSpeedMin,self.chargeSpeedMax)

                # if we're a runner we run during charges *except when near an edge (otherwise we tend to fly off easily)
                if self.run and distRaw > self.runDistMin:
                    self._leadAmount = 0.3
                    self._running = True
                    self.node.run = 1.0
                else:
                    self._leadAmont = 0.01
                    self._running = False
                    self.node.run = 0.0

            self.node.moveLeftRight = toTarget.x() * self._chargeSpeed
            self.node.moveUpDown = toTarget.z() * -1.0*self._chargeSpeed

        elif self._mode == 'wait':
            # every now and then, aim towards our target.. other than that, just stand there
            if bs.getGameTime()%1234 < 100:
                self.node.moveLeftRight = toTarget.x() * (400.0/33000)
                self.node.moveUpDown = toTarget.z() * (-400.0/33000)
            else:
                self.node.moveLeftRight = 0
                self.node.moveUpDown = 0

        elif self._mode == 'flee':

            # even if we're a runner, only run till we get away from our target (if we keep running we tend to run off edges)
            if self.run and dist < 3.0:
                self._running = True
                self.node.run = 1.0
            else:
                self._running = False
                self.node.run = 0.0
            self.node.moveLeftRight = toTarget.x() * -1.0
            self.node.moveUpDown = toTarget.z()

        # we might wanna switch states unless we're doing a throw (in which case thats our sole concern)
        if self._mode != 'throw':

            # if we're currently charging, keep track of how far we are from our target..
            # when this value increases it means our charge is over (ran by them or something)
            if self._mode == 'charge':
                if self._chargeClosingIn and dist < 3.0 and dist > self._lastChargeDist:
                    self._chargeClosingIn = False
                self._lastChargeDist = dist

            # if we have a clean shot, throw!
            if dist >= self.throwDistMin and dist < self.throwDistMax and random.random() < self.throwiness and canAttack:
                self._mode = 'throw'
                self._leadAmount = (0.4+random.random()*0.6) if distRaw > 4.0 else (0.1+random.random()*0.4)
                self._haveDroppedThrowBomb = False
                self._throwReleaseTime = bs.getGameTime() + (1.0/self.throwRate)*(800 + int(1300*random.random()))

            # if we're static, always charge (which for us means barely move)
            elif self.static:
                self._mode = 'wait'
                
            # if we're too close to charge (and arent in the middle of an existing charge) run away
            elif dist < self.chargeDistMin and not self._chargeClosingIn:
                # ..unless we're near an edge, in which case we got no choice but to charge..
                if self._map()._isPointNearEdge(ourPos,self._running):
                    if self._mode != 'charge':
                        self._mode = 'charge'
                        self._leadAmount = 0.2
                        self._chargeClosingIn = True
                        self._lastChargeDist = dist
                else:
                    self._mode = 'flee'

            # we're within charging distance, backed against an edge, or farther than our max throw distance.. chaaarge!
            elif dist < self.chargeDistMax or dist > self.throwDistMax or self._map()._isPointNearEdge(ourPos,self._running):
                if self._mode != 'charge':
                    self._mode = 'charge'
                    self._leadAmount = 0.01
                    self._chargeClosingIn = True
                    self._lastChargeDist = dist

            # we're too close to throw but too far to charge - either run away or just chill if we're near an edge
            elif dist < self.throwDistMin:
                # charge if either we're within charge range or cant retreat to throw
                self._mode = 'flee'

            # do some awesome jumps if we're running
            if ((self._running and dist > 1.2 and dist < 2.2 and bs.getGameTime()-self._lastJumpTime > 1000)
                or (self.bouncy and bs.getGameTime()-self._lastJumpTime > 400 and random.random() < 0.5)):
                self._lastJumpTime = bs.getGameTime()
                self.node.jumpPressed = True
                self.node.jumpPressed = False

                
            # throw punches when real close
            if dist < (1.6 if self._running else 1.2) and canAttack:
                if random.random() < self.punchiness:
                    self.onPunchPress()
                    self.onPunchRelease()

    def __superHandleMessage(self,m):
        super(SpazBot,self).handleMessage(m)

    def onPunched(self,damage):
        """
        Method override; sends a bs.SpazBotPunchedMessage to the current activity.
        """
        bs.getActivity().handleMessage(SpazBotPunchedMessage(self,damage))

    def onFinalize(self):
        Spaz.onFinalize(self)
        # we're being torn down; release
        # our callback(s) so there's no chance of them
        # keeping activities or other things alive..
        self.updateCallback = None

        
    def handleMessage(self,m):
        self._handleMessageSanityCheck()

        # keep track of if we're being held and by who most recently
        if isinstance(m,bs.PickedUpMessage):
            self.__superHandleMessage(m) # augment standard behavior
            self.heldCount += 1
            pickedUpBy = m.node.sourcePlayer
            if pickedUpBy is not None and pickedUpBy.exists():
                self.lastPlayerHeldBy = pickedUpBy

        elif isinstance(m,bs.DroppedMessage):
            self.__superHandleMessage(m) # augment standard behavior
            self.heldCount -= 1
            if self.heldCount < 0:
                print "ERROR: spaz heldCount < 0"
            # let's count someone dropping us as an attack..
            try:
                if m.node.exists(): pickedUpBy = m.node.sourcePlayer
                else: pickedUpBy = bs.Player(None) # empty player ref
            except Exception,e:
                print 'EXC on SpazBot DroppedMessage:',e
                pickedUpBy = bs.Player(None) # empty player ref

            if pickedUpBy.exists():
                self.lastPlayerAttackedBy = pickedUpBy
                self.lastAttackedTime = bs.getGameTime()
                self.lastAttackedType = ('pickedUp','default')
            
        elif isinstance(m,bs.DieMessage):

            # jasonhu5
            if self.isBotFriendly:
                self._player.setActor(self._ownerPlayerSpaz)
                self._ownerPlayerSpaz.connectControlsToPlayer(self._player)
            # 

            # report normal deaths for scoring purposes
            if not self._dead and not m.immediate:

                # if this guy was being held at the time of death, the holder is the killer
                if self.heldCount > 0 and self.lastPlayerHeldBy is not None and self.lastPlayerHeldBy.exists():
                    killerPlayer = self.lastPlayerHeldBy
                else:
                    # otherwise if they were attacked by someone in the last few seconds
                    # that person's the killer.. otherwise it was a suicide
                    if self.lastPlayerAttackedBy is not None and self.lastPlayerAttackedBy.exists() and bs.getGameTime() - self.lastAttackedTime < 4000:
                        killerPlayer = self.lastPlayerAttackedBy
                    else:
                        killerPlayer = None
                activity = self._activity()

                if killerPlayer is not None and not killerPlayer.exists(): killerPlayer = None
                if activity is not None: activity.handleMessage(SpazBotDeathMessage(self,killerPlayer,m.how))
            self.__superHandleMessage(m) # augment standard behavior

        # keep track of the player who last hit us for point rewarding
        elif isinstance(m,bs.HitMessage):
            if m.sourcePlayer is not None and m.sourcePlayer.exists():
                self.lastPlayerAttackedBy = m.sourcePlayer
                self.lastAttackedTime = bs.getGameTime()
                self.lastAttackedType = (m.hitType,m.hitSubType)
            self.__superHandleMessage(m)
        else:
            Spaz.handleMessage(self,m)
      
# jasonhu5 
class SuicideBomber(SpazBot):

    character = 'Jack Morgan'
    run = True
    chargeDistMin = 0.0
    chargeDistMax = 9999
    chargeSpeedMin = 1.0
    chargeSpeedMax = 1.0
    throwDistMin = 9999
    throwDistMax = 9999
    startCursed = True
    pointsMult = 3
    isBotFriendly = True
# 

class BunnyBot(SpazBot):
    """
    category: Bot Classes
    
    A speedy attacking melee bot.
    """

    color=(1,1,1)
    highlight=(1.0,0.5,0.5)
    character = 'Easter Bunny'
    punchiness = 1.0
    run = True
    bouncy = True
    defaultBoxingGloves = True
    chargeDistMin = 10.0
    chargeDistMax = 9999.0
    chargeSpeedMin = 1.0
    chargeSpeedMax = 1.0
    throwDistMin = 9999
    throwDistMax = 9999
    pointsMult = 2

class BomberBot(SpazBot):
    """
    category: Bot Classes
    
    A bot that throws regular bombs
    and occasionally punches.
    """
    character='Spaz'
    punchiness=0.3

class BomberBotLame(BomberBot):
    """
    category: Bot Classes
    
    A less aggressive yellow version of bs.BomberBot.
    """
    color=gLameBotColor
    highlight=gLameBotHighlight
    punchiness = 0.2
    throwRate = 0.7
    throwiness = 0.1
    chargeSpeedMin = 0.6
    chargeSpeedMax = 0.6

class BomberBotStaticLame(BomberBotLame):
    """
    category: Bot Classes
    
    A less aggressive yellow version of bs.BomberBot
    who generally stays in one place.
    """
    static = True
    throwDistMin = 0.0

class BomberBotStatic(BomberBot):
    """
    category: Bot Classes
    
    A version of bs.BomberBot
    who generally stays in one place.
    """
    static = True
    throwDistMin = 0.0


class BomberBotPro(BomberBot):
    """
    category: Bot Classes
    
    A more aggressive red version of bs.BomberBot.
    """
    pointsMult = 2
    color=gProBotColor
    highlight = gProBotHighlight
    defaultBombCount = 3
    defaultBoxingGloves = True
    punchiness = 0.7
    throwRate = 1.3
    run = True
    runDistMin = 6.0

class BomberBotProShielded(BomberBotPro):
    """
    category: Bot Classes
    
    A more aggressive red version of bs.BomberBot
    who starts with shields.
    """
    pointsMult = 3
    defaultShields = True

class BomberBotProStatic(BomberBotPro):
    """
    category: Bot Classes
    
    A more aggressive red version of bs.BomberBot
    who generally stays in one place.
    """
    static = True
    throwDistMin = 0.0

class BomberBotProStaticShielded(BomberBotProShielded):
    """
    category: Bot Classes
    
    A more aggressive red version of bs.BomberBot
    who starts with shields and
    who generally stays in one place.
    """
    static = True
    throwDistMin = 0.0

class BomberBotProStaticShielded(BomberBotProShielded):
    """
    category: Bot Classes
    
    A more aggressive red version of bs.BomberBot
    who starts with shields and
    who generally stays in one place.
    """
    static = True
    # throwRate = 2.0
    throwDistMin = 0.0
    defaultBombType = 'impact'
    # throwiness = 5.0

class ToughGuyBot(SpazBot):
    """
    category: Bot Classes
    
    A manly bot who walks and punches things.
    """
    character = 'Kronk'
    punchiness = 0.9
    chargeDistMax = 9999.0
    chargeSpeedMin = 1.0
    chargeSpeedMax = 1.0
    throwDistMin = 9999
    throwDistMax = 9999

class ToughGuyBotLame(ToughGuyBot):
    """
    category: Bot Classes
    
    A less aggressive yellow version of bs.ToughGuyBot.
    """
    color=gLameBotColor
    highlight=gLameBotHighlight
    punchiness = 0.3
    chargeSpeedMin = 0.6
    chargeSpeedMax = 0.6

class ToughGuyBotPro(ToughGuyBot):
    """
    category: Bot Classes
    
    A more aggressive red version of bs.ToughGuyBot.
    """
    color=gProBotColor
    highlight=gProBotHighlight
    run = True
    runDistMin = 4.0
    defaultBoxingGloves = True
    punchiness = 0.95
    pointsMult = 2

class ToughGuyBotProShielded(ToughGuyBotPro):
    """
    category: Bot Classes
    
    A more aggressive version of bs.ToughGuyBot
    who starts with shields.
    """
    defaultShields = True
    pointsMult = 3

class NinjaBot(SpazBot):
    """
    category: Bot Classes
    
    A speedy attacking melee bot.
    """

    character = 'Snake Shadow'
    punchiness = 1.0
    run = True
    chargeDistMin = 10.0
    chargeDistMax = 9999.0
    chargeSpeedMin = 1.0
    chargeSpeedMax = 1.0
    throwDistMin = 9999
    throwDistMax = 9999
    pointsMult = 2
    
class NinjaBotPro(NinjaBot):
    """
    category: Bot Classes
    
    A more aggressive red bs.NinjaBot.
    """
    color=gProBotColor
    highlight=gProBotHighlight
    defaultShields = True
    defaultBoxingGloves = True
    pointsMult = 3

class NinjaBotProShielded(NinjaBotPro):
    """
    category: Bot Classes
    
    A more aggressive red bs.NinjaBot
    who starts with shields.
    """
    defaultShields = True
    pointsMult = 4

class ChickBot(SpazBot):
    """
    category: Bot Classes
    
    A slow moving bot with impact bombs.
    """
    character = 'Zoe'
    punchiness = 0.75
    throwiness = 0.7
    chargeDistMax = 1.0
    chargeSpeedMin = 0.3
    chargeSpeedMax = 0.5
    throwDistMin = 3.5
    throwDistMax = 5.5
    defaultBombType = 'impact'
    pointsMult = 2

class ChickBotStatic(ChickBot):
    """
    category: Bot Classes
    
    A bs.ChickBot who generally stays in one place.
    """
    static = True
    throwDistMin = 0.0

class ChickBotPro(ChickBot):
    """
    category: Bot Classes
    
    A more aggressive red version of bs.ChickBot.
    """
    color=gProBotColor
    highlight=gProBotHighlight
    defaultBombCount = 3
    defaultBoxingGloves = True
    chargeSpeedMin = 1.0
    chargeSpeedMax = 1.0
    punchiness = 0.9
    throwRate = 1.3
    run = True
    runDistMin = 6.0
    pointsMult = 3

class ChickBotProShielded(ChickBotPro):
    """
    category: Bot Classes
    
    A more aggressive red version of bs.ChickBot
    who starts with shields.
    """
    defaultShields = True
    pointsMult = 4

class MelBot(SpazBot):
    """
    category: Bot Classes
    
    A crazy bot who runs and throws sticky bombs.
    """
    character = 'Mel'
    punchiness = 0.9
    throwiness = 1.0
    run = True
    chargeDistMin = 4.0
    chargeDistMax = 10.0
    chargeSpeedMin = 1.0
    chargeSpeedMax = 1.0
    throwDistMin = 0.0
    throwDistMax = 4.0
    throwRate = 2.0
    defaultBombType = 'sticky'
    defaultBombCount = 3
    pointsMult = 3

class MelBotStatic(MelBot):
    """
    category: Bot Classes
    
    A crazy bot who throws sticky-bombs but generally stays in one place.
    """
    static = True
    throwDistMin = 0.0
    throwDistMax = 10.0
    
class MelDuperBot(MelBot):
    """
    A crazy bot who runs and throws sticky bombs.
    He has a shield and doesn't like you as a person
    and will do everything to make you puke and give
    you headaches. Only available in Nightmare gamemode.
    """
    color=gProBotColor
    highlight=gProBotHighlight
    defaultShields = True
    defaultBoxingGloves = True
    throwRate = 3.0
    defaultBombCount = 5
    pointsMult = 4

class PirateBot(SpazBot):
    """
    category: Bot Classes
    
    A bot who runs and explodes in 5 seconds.
    """
    character = 'Jack Morgan'
    run = True
    chargeDistMin = 0.0
    chargeDistMax = 9999
    chargeSpeedMin = 1.0
    chargeSpeedMax = 1.0
    throwDistMin = 9999
    throwDistMax = 9999
    startCursed = True
    pointsMult = 3

class PirateBotNoTimeLimit(PirateBot):
    """
    category: Bot Classes
    
    A bot who runs but does not explode on his own.
    """
    curseTime = -1

class PirateBotShielded(PirateBot):
    """
    category: Bot Classes
    
    A bs.PirateBot who starts with shields.
    """
    defaultShields = True
    pointsMult = 5
	
class FrostyBot(SpazBot):
    """
    category: Bot Classes
    
    A bot that throws ice bombs
    and occasionally punches.
    """
    character='Frosty'
    punchiness=0.3
    color=(0.5,0.5,1)
    highlight=(1,0.5,0)
    defaultBombType = 'ice'
    pointsMult = 4
    
class FrostyBotStatic(FrostyBot):
    """
    category: Bot Classes
    
    A bot that throws ice bombs
    and stays in one place most of the time.
    """
    static = True
    throwDistMin = 0.0
    
class FrostyBotShielded(FrostyBot):
    """
    category: Bot Classes
    
    A crazed maniac. This time with shields!
    """
    color=(0.2,0.2,1)
    highlight=(1,0,0)
    defaultShields = True
    pointsMult = 6
	
class AgentBot(MelBot):
    """
    category: Bot Classes
    
    A crazy bot who runs and throws impact bombs.
    """
    character = 'Agent Johnson'
    color=(0.1,0.1,0.1)
    highlight=(0.1,0.1,0.1)
    throwRate = 3
    defaultBombType = 'impact'
    pointsMult = 2

class AgentBotShielded(AgentBot):
    """
    category: Bot Classes
    
    Agent Bot with armor
    """
    color=(1,0.1,0.1)
    highlight=(0.3,0.1,0.1)
    defaultShields = True
    pointsMult = 3
    
class CyborgBot(SpazBot):
    """
    category: Bot Classes
    
    A slow moving bot with combat bombs.
    """
    character = 'B-9000'
    highlight = (0,1,1)
    punchiness = 1.0
    throwiness = 1.0
    chargeDistMax = 1.0
    chargeSpeedMin = 0.3
    chargeSpeedMax = 0.5
    throwRate = 1.5
    throwDistMin = 4.5
    throwDistMax = 6.5
    defaultBombType = 'combat'
    pointsMult = 2
	
class SpyBot(SpazBot):
    """
    category: Bot Classes
    
    A slow moving bot that ocasionally throws land mines.
    """
    character = 'Spy'
    color=(0.1,0.1,0.1)
    highlight=(1,1,1)
    punchiness = 1
    throwiness = 0.5
    chargeDistMax = 4
    throwRate = 1.5
    chargeSpeedMin = 1
    chargeSpeedMax = 1
    throwDistMin = 3
    throwDistMax = 9999
    defaultBombCount = 5
    defaultBombType = 'landMine'
    pointsMult = 2
	
class LooieBot(SpazBot):
    """
    category: Bot Classes
    
    A crazed maniac (probably on drugs) that jumps everywhere, throws bombs everywhere and will punch you hard if you're not careful.
    """

    color=(1,0.7,0.0)
    highlight=(1,1,1)
    character = 'Looie'
    punchiness = 0.8
    throwiness = 1.0
    run = True
    bouncy = True
    chargeDistMin = 10.0
    chargeDistMax = 9999.0
    chargeSpeedMin = 1.0
    chargeSpeedMax = 1.0
    throwDistMin = 2
    throwDistMax = 9999
    pointsMult = 4
    throwRate = 10.0
    defaultBombCount = 6
    
class LooieBotShielded(LooieBot):
    """
    category: Bot Classes
    
    A crazed maniac. This time with shields!
    """
    color=(1,0.0,0.0)
    highlight=(1,1,1)
    defaultShields = True
    pointsMult = 5
    
class BotSet(object):
    """
    category: Bot Classes
    
    A container/controller for one or more bs.SpazBots.
    """
    def __init__(self):
        """
        Create a bot-set.
        """
        # we spread our bots out over a few lists so we can update them in a staggered fashion
        self._botListCount = 5
        self._botAddList = 0
        self._botUpdateList = 0
        self._botLists = [[] for i in range(self._botListCount)]
        self._spawnSound = bs.getSound('spawn')
        self._spawningCount = 0
        self.startMoving()

    def __del__(self):
        self.clear()

    def spawnBot(self,botType,pos,spawnTime=3000,onSpawnCall=None):
        bsUtils.Spawner(pt=pos,
                        spawnTime=spawnTime,
                        sendSpawnMessage=False,
                        spawnCallback=bs.Call(self._spawnBot,botType,pos,onSpawnCall))
        self._spawningCount += 1

    def _spawnBot(self,botType,pos,onSpawnCall):
        spaz = botType()
        bs.playSound(self._spawnSound,position=pos)
        spaz.node.handleMessage("flash")
        spaz.node.isAreaOfInterest = 0
        spaz.handleMessage(bs.StandMessage(pos,random.uniform(0,360)))
        self.addBot(spaz)
        self._spawningCount -= 1
        if onSpawnCall is not None: onSpawnCall(spaz)
        
    def haveLivingBots(self):
        """
        Returns whether any bots in the set are alive or in the process of spawning.
        """
        haveLiving = any((any((not a._dead for a in l)) for l in self._botLists))
        haveSpawning = True if self._spawningCount > 0 else False
        return (haveLiving or haveSpawning)


    def getLivingBots(self):
        """
        Returns the living bots in the set.
        """
        bots = []
        for l in self._botLists:
            for b in l:
                if not b._dead: bots.append(b)
        return bots

    def _update(self):

        # update one of our bot lists each time through..
        # first off, remove dead bots from the list
        # (we check exists() here instead of dead.. we want to keep them around even if they're just a corpse)
        try:
            botList = self._botLists[self._botUpdateList] = [b for b in self._botLists[self._botUpdateList] if b.exists()]
        except Exception:
            bs.printException("error updating bot list: "+str(self._botLists[self._botUpdateList]))
        self._botUpdateList = (self._botUpdateList+1)%self._botListCount

        # update our list of player points for the bots to use
        playerPts = []
        for player in bs.getActivity().players:
            try:
                if player.isAlive():
                    playerPts.append((bs.Vector(*player.actor.node.position),
                                     bs.Vector(*player.actor.node.velocity)))
            except Exception:
                bs.printException('error on bot-set _update')

        for b in botList:
            b._setPlayerPts(playerPts)
            b._updateAI()

    def clear(self):
        """
        Immediately clear out any bots in the set.
        """
        # dont do this if the activity is shutting down or dead
        activity = bs.getActivity(exceptionOnNone=False)
        if activity is None or activity.isFinalized(): return
        
        for i in range(len(self._botLists)):
            for b in self._botLists[i]:
                b.handleMessage(bs.DieMessage(immediate=True))
            self._botLists[i] = []
        
    def celebrate(self,duration):
        """
        Tell all living bots in the set to celebrate momentarily
        while continuing onward with their evil bot activities.
        """
        for l in self._botLists:
            for b in l:
                if b.node.exists():
                    b.node.handleMessage('celebrate',duration)

    def startMoving(self):
        self._botUpdateTimer = bs.Timer(50,bs.WeakCall(self._update),repeat=True)
                    
    def stopMoving(self):
        """
        Tell all bots to stop moving and stops
        updating their AI.
        Useful when players have won and you want the
        enemy bots to just stand and look bewildered.
        """
        self._botUpdateTimer = None
        for l in self._botLists:
            for b in l:
                if b.node.exists():
                    b.node.moveLeftRight = 0
                    b.node.moveUpDown = 0
        
    def finalCelebrate(self):
        """
        Tell all bots in the set to stop what they were doing
        and just jump around and celebrate.  Use this when
        the bots have won a game.
        """
        self._botUpdateTimer = None
        # at this point stop doing anything but jumping and celebrating
        for l in self._botLists:
            for b in l:
                if b.node.exists():
                    b.node.moveLeftRight = 0
                    b.node.moveUpDown = 0
                    bs.gameTimer(random.randrange(0,500),bs.Call(b.node.handleMessage,'celebrate',10000))
                    jumpDuration = random.randrange(400,500)
                    j = random.randrange(0,200)
                    for i in range(10):
                        b.node.jumpPressed = True
                        b.node.jumpPressed = False
                        j += jumpDuration
                    bs.gameTimer(random.randrange(0,1000),bs.Call(b.node.handleMessage,'attackSound'))
                    bs.gameTimer(random.randrange(1000,2000),bs.Call(b.node.handleMessage,'attackSound'))
                    bs.gameTimer(random.randrange(2000,3000),bs.Call(b.node.handleMessage,'attackSound'))

    def addBot(self,bot):
        """
        Add a bs.SpazBot instance to the set.
        """
        self._botLists[self._botAddList].append(bot)
        self._botAddList = (self._botAddList+1)%self._botListCount


# define our built-in characters...


###############  SPAZ   ##################
t = Appearance("Spaz")

t.colorTexture = "neoSpazColor"
t.colorMaskTexture = "neoSpazColorMask"

t.iconTexture = "neoSpazIcon"
t.iconMaskTexture = "neoSpazIconColorMask"

t.headModel = "neoSpazHead"
t.torsoModel = "neoSpazTorso"
t.pelvisModel = "neoSpazPelvis"
t.upperArmModel = "neoSpazUpperArm"
t.foreArmModel = "neoSpazForeArm"
t.handModel = "neoSpazHand"
t.upperLegModel = "neoSpazUpperLeg"
t.lowerLegModel = "neoSpazLowerLeg"
t.toesModel = "neoSpazToes"

t.jumpSounds=["spazJump01",
              "spazJump02",
              "spazJump03",
              "spazJump04"]
# t.attackSounds=["spazAttack01",
#                 "spazAttack02",
#                 "spazAttack03",
#                 "spazAttack04"]
t.attackSounds=["jsnh1",
                "jsnh1",
                "jsnh1",
                "jsnh1"]
t.impactSounds=["spazImpact01",
                "spazImpact02",
                "spazImpact03",
                "spazImpact04"]
t.deathSounds=["spazDeath01"]
t.pickupSounds=["spazPickup01"]
t.fallSounds=["spazFall01"]

t.style = 'spaz'


###############  Zoe   ##################
t = Appearance("Zoe")

t.colorTexture = "zoeColor"
t.colorMaskTexture = "zoeColorMask"

t.defaultColor = (0.6,0.6,0.6)
t.defaultHighlight = (0,1,0)

t.iconTexture = "zoeIcon"
t.iconMaskTexture = "zoeIconColorMask"

t.headModel = "zoeHead"
t.torsoModel = "zoeTorso"
t.pelvisModel = "zoePelvis"
t.upperArmModel = "zoeUpperArm"
t.foreArmModel = "zoeForeArm"
t.handModel = "zoeHand"
t.upperLegModel = "zoeUpperLeg"
t.lowerLegModel = "zoeLowerLeg"
t.toesModel = "zoeToes"

t.jumpSounds=["zoeJump01",
              "zoeJump02",
              "zoeJump03"]
t.attackSounds=["zoeAttack01",
                "zoeAttack02",
                "zoeAttack03",
                "zoeAttack04"]
t.impactSounds=["zoeImpact01",
                "zoeImpact02",
                "zoeImpact03",
                "zoeImpact04"]
t.deathSounds=["zoeDeath01"]
t.pickupSounds=["zoePickup01"]
t.fallSounds=["zoeFall01"]

t.style = 'female'


###############  Ninja   ##################
t = Appearance("Snake Shadow")

t.colorTexture = "ninjaColor"
t.colorMaskTexture = "ninjaColorMask"

t.defaultColor = (1,1,1)
t.defaultHighlight = (0.55,0.8,0.55)

t.iconTexture = "ninjaIcon"
t.iconMaskTexture = "ninjaIconColorMask"

t.headModel = "ninjaHead"
t.torsoModel = "ninjaTorso"
t.pelvisModel = "ninjaPelvis"
t.upperArmModel = "ninjaUpperArm"
t.foreArmModel = "ninjaForeArm"
t.handModel = "ninjaHand"
t.upperLegModel = "ninjaUpperLeg"
t.lowerLegModel = "ninjaLowerLeg"
t.toesModel = "ninjaToes"

ninjaAttacks = ['ninjaAttack'+str(i+1)+'' for i in range(7)]
ninjaHits = ['ninjaHit'+str(i+1)+'' for i in range(8)]
ninjaJumps = ['ninjaAttack'+str(i+1)+'' for i in range(7)]

t.jumpSounds=ninjaJumps
t.attackSounds=ninjaAttacks
t.impactSounds=ninjaHits
t.deathSounds=["ninjaDeath1"]
t.pickupSounds=ninjaAttacks
t.fallSounds=["ninjaFall1"]

t.style = 'ninja'


###############  Kronk   ##################
t = Appearance("Kronk")

t.colorTexture = "kronk"
t.colorMaskTexture = "kronkColorMask"

t.defaultColor = (0.4,0.5,0.4)
t.defaultHighlight = (1,0.5,0.3)

t.iconTexture = "kronkIcon"
t.iconMaskTexture = "kronkIconColorMask"

t.headModel = "kronkHead"
t.torsoModel = "kronkTorso"
t.pelvisModel = "kronkPelvis"
t.upperArmModel = "kronkUpperArm"
t.foreArmModel = "kronkForeArm"
t.handModel = "kronkHand"
t.upperLegModel = "kronkUpperLeg"
t.lowerLegModel = "kronkLowerLeg"
t.toesModel = "kronkToes"

kronkSounds = ["kronk1",
              "kronk2",
              "kronk3",
              "kronk4",
              "kronk5",
              "kronk6",
              "kronk7",
              "kronk8",
              "kronk9",
              "kronk10"]
t.jumpSounds=kronkSounds
t.attackSounds=kronkSounds
t.impactSounds=kronkSounds
t.deathSounds=["kronkDeath"]
t.pickupSounds=kronkSounds
t.fallSounds=["kronkFall"]

t.style = 'kronk'


###############  MEL   ##################
t = Appearance("Mel")

t.colorTexture = "melColor"
t.colorMaskTexture = "melColorMask"

t.defaultColor = (1,1,1)
t.defaultHighlight = (0.1,0.6,0.1)

t.iconTexture = "melIcon"
t.iconMaskTexture = "melIconColorMask"

t.headModel =     "melHead"
t.torsoModel =    "melTorso"
t.pelvisModel = "kronkPelvis"
t.upperArmModel = "melUpperArm"
t.foreArmModel =  "melForeArm"
t.handModel =     "melHand"
t.upperLegModel = "melUpperLeg"
t.lowerLegModel = "melLowerLeg"
t.toesModel =     "melToes"

melSounds = ["mel01",
             "mel02",
             "mel03",
             "mel04",
             "mel05",
             "mel06",
             "mel07",
             "mel08",
             "mel09",
             "mel10"]

t.attackSounds = melSounds
t.jumpSounds = melSounds
t.impactSounds = melSounds
t.deathSounds=["melDeath01"]
t.pickupSounds = melSounds
t.fallSounds=["melFall01"]

t.style = 'mel'


###############  Jack Morgan   ##################

t = Appearance("Jack Morgan")

# t.colorTexture = "jackColor"
# jasonhu5
t.colorTexture = "jackColorMod"
# 
t.colorMaskTexture = "jackColorMask"

t.defaultColor = (1,0.2,0.1)
t.defaultHighlight = (1,1,0)

t.iconTexture = "jackIcon"
t.iconMaskTexture = "jackIconColorMask"

# t.headModel =     "jackHead"
# jasonhu5
t.headModel = "jackHeadMod"
# 
t.torsoModel =    "jackTorso"
t.pelvisModel = "kronkPelvis"
t.upperArmModel = "jackUpperArm"
t.foreArmModel =  "jackForeArm"
t.handModel =     "jackHand"
t.upperLegModel = "jackUpperLeg"
t.lowerLegModel = "jackLowerLeg"
t.toesModel =     "jackToes"

hitSounds = ["jackHit01",
             "jackHit02",
             "jackHit03",
             "jackHit04",
             "jackHit05",
             "jackHit06",
             "jackHit07"]

sounds = ["jack01",
          "jack02",
          "jack03",
          "jack04",
          "jack05",
          "jack06"]

t.attackSounds = sounds
t.jumpSounds = sounds
t.impactSounds = hitSounds
t.deathSounds=["jackDeath01"]
t.pickupSounds = sounds
t.fallSounds=["jackFall01"]

t.style = 'pirate'


###############  SANTA   ##################

t = Appearance("Santa Claus")

t.colorTexture = "santaColor"
t.colorMaskTexture = "santaColorMask"

t.defaultColor = (1,0,0)
t.defaultHighlight = (1,1,1)

t.iconTexture = "santaIcon"
t.iconMaskTexture = "santaIconColorMask"

t.headModel =     "santaHead"
t.torsoModel =    "santaTorso"
t.pelvisModel = "kronkPelvis"
t.upperArmModel = "santaUpperArm"
t.foreArmModel =  "santaForeArm"
t.handModel =     "santaHand"
t.upperLegModel = "santaUpperLeg"
t.lowerLegModel = "santaLowerLeg"
t.toesModel =     "santaToes"

hitSounds = ['santaHit01','santaHit02','santaHit03','santaHit04']
sounds = ['santa01','santa02','santa03','santa04','santa05']

t.attackSounds = sounds
t.jumpSounds = sounds
t.impactSounds = hitSounds
t.deathSounds=["santaDeath"]
t.pickupSounds = sounds
t.fallSounds=["santaFall"]

t.style = 'santa'

###############  FROSTY   ##################

t = Appearance("Frosty")

t.colorTexture = "frostyColor"
t.colorMaskTexture = "frostyColorMask"

t.defaultColor = (0.5,0.5,1)
t.defaultHighlight = (1,0.5,0)

t.iconTexture = "frostyIcon"
t.iconMaskTexture = "frostyIconColorMask"

t.headModel =     "frostyHead"
t.torsoModel =    "frostyTorso"
t.pelvisModel = "frostyPelvis"
t.upperArmModel = "frostyUpperArm"
t.foreArmModel =  "frostyForeArm"
t.handModel =     "frostyHand"
t.upperLegModel = "frostyUpperLeg"
t.lowerLegModel = "frostyLowerLeg"
t.toesModel =     "frostyToes"

frostySounds = ['frosty01','frosty02','frosty03','frosty04','frosty05']
frostyHitSounds = ['frostyHit01','frostyHit02','frostyHit03']

t.attackSounds = frostySounds
t.jumpSounds = frostySounds
t.impactSounds = frostyHitSounds
t.deathSounds=["frostyDeath"]
t.pickupSounds = frostySounds
t.fallSounds=["frostyFall"]

t.style = 'frosty'

###############  BONES  ##################

t = Appearance("Bones")

# t.colorTexture = "bonesColor"
# jasonhu5
t.colorTexture = "bonesColorMod"
# 
t.colorMaskTexture = "bonesColorMask"

t.defaultColor = (0.6,0.9,1)
t.defaultHighlight = (0.6,0.9,1)

t.iconTexture = "bonesIcon"
t.iconMaskTexture = "bonesIconColorMask"

# t.headModel =     "bonesHead"
# jasonhu5
t.headModel = "bonesHeadMod"
# 
t.torsoModel =    "bonesTorso"
t.pelvisModel =   "bonesPelvis"
t.upperArmModel = "bonesUpperArm"
t.foreArmModel =  "bonesForeArm"
t.handModel =     "bonesHand"
t.upperLegModel = "bonesUpperLeg"
t.lowerLegModel = "bonesLowerLeg"
t.toesModel =     "bonesToes"

bonesSounds =    ['bones1','bones2','bones3']
bonesHitSounds = ['bones1','bones2','bones3']

t.attackSounds = bonesSounds
t.jumpSounds = bonesSounds
t.impactSounds = bonesHitSounds
t.deathSounds=["bonesDeath"]
t.pickupSounds = bonesSounds
t.fallSounds=["bonesFall"]

t.style = 'bones'

# bear ###################################

t = Appearance("Bernard")

t.colorTexture = "bearColor"
t.colorMaskTexture = "bearColorMask"

t.defaultColor = (0.7,0.5,0.0)
#t.defaultHighlight = (0.6,0.5,0.8)

t.iconTexture = "bearIcon"
t.iconMaskTexture = "bearIconColorMask"

t.headModel =     "bearHead"
t.torsoModel =    "bearTorso"
t.pelvisModel =   "bearPelvis"
t.upperArmModel = "bearUpperArm"
t.foreArmModel =  "bearForeArm"
t.handModel =     "bearHand"
t.upperLegModel = "bearUpperLeg"
t.lowerLegModel = "bearLowerLeg"
t.toesModel =     "bearToes"

bearSounds =    ['bear1','bear2','bear3','bear4']
bearHitSounds = ['bearHit1','bearHit2']

t.attackSounds = bearSounds
t.jumpSounds = bearSounds
t.impactSounds = bearHitSounds
t.deathSounds=["bearDeath"]
t.pickupSounds = bearSounds
t.fallSounds=["bearFall"]

t.style = 'bear'

# Penguin ###################################

t = Appearance("Pascal")

t.colorTexture = "penguinColor"
t.colorMaskTexture = "penguinColorMask"

t.defaultColor = (0.3,0.5,0.8)
t.defaultHighlight = (1,0,0)

t.iconTexture = "penguinIcon"
t.iconMaskTexture = "penguinIconColorMask"

t.headModel =     "penguinHead"
t.torsoModel =    "penguinTorso"
t.pelvisModel =   "penguinPelvis"
t.upperArmModel = "penguinUpperArm"
t.foreArmModel =  "penguinForeArm"
t.handModel =     "penguinHand"
t.upperLegModel = "penguinUpperLeg"
t.lowerLegModel = "penguinLowerLeg"
t.toesModel =     "penguinToes"

penguinSounds =    ['penguin1','penguin2','penguin3','penguin4']
penguinHitSounds = ['penguinHit1','penguinHit2']

t.attackSounds = penguinSounds
t.jumpSounds = penguinSounds
t.impactSounds = penguinHitSounds
t.deathSounds=["penguinDeath"]
t.pickupSounds = penguinSounds
t.fallSounds=["penguinFall"]

t.style = 'penguin'


# Ali ###################################
t = Appearance("Taobao Mascot")
t.colorTexture = "aliColor"
t.colorMaskTexture = "aliColorMask"
t.defaultColor = (1,0.5,0)
t.defaultHighlight = (1,1,1)
t.iconTexture = "aliIcon"
t.iconMaskTexture = "aliIconColorMask"
t.headModel =     "aliHead"
t.torsoModel =    "aliTorso"
t.pelvisModel =   "aliPelvis"
t.upperArmModel = "aliUpperArm"
t.foreArmModel =  "aliForeArm"
t.handModel =     "aliHand"
t.upperLegModel = "aliUpperLeg"
t.lowerLegModel = "aliLowerLeg"
t.toesModel =     "aliToes"
aliSounds =    ['ali1','ali2','ali3','ali4']
aliHitSounds = ['aliHit1','aliHit2']
t.attackSounds = aliSounds
t.jumpSounds = aliSounds
t.impactSounds = aliHitSounds
t.deathSounds=["aliDeath"]
t.pickupSounds = aliSounds
t.fallSounds=["aliFall"]
t.style = 'ali'

# cyborg ###################################
t = Appearance("B-9000")
t.colorTexture = "cyborgColor"
t.colorMaskTexture = "cyborgColorMask"
t.defaultColor = (0.5,0.5,0.5)
t.defaultHighlight = (1,0,0)
t.iconTexture = "cyborgIcon"
t.iconMaskTexture = "cyborgIconColorMask"
t.headModel =     "cyborgHead"
t.torsoModel =    "cyborgTorso"
t.pelvisModel =   "cyborgPelvis"
t.upperArmModel = "cyborgUpperArm"
t.foreArmModel =  "cyborgForeArm"
t.handModel =     "cyborgHand"
t.upperLegModel = "cyborgUpperLeg"
t.lowerLegModel = "cyborgLowerLeg"
t.toesModel =     "cyborgToes"
cyborgSounds =    ['cyborg1','cyborg2','cyborg3','cyborg4']
cyborgHitSounds = ['cyborgHit1','cyborgHit2']
t.attackSounds = cyborgSounds
t.jumpSounds = cyborgSounds
t.impactSounds = cyborgHitSounds
t.deathSounds=["cyborgDeath"]
t.pickupSounds = cyborgSounds
t.fallSounds=["cyborgFall"]
t.style = 'cyborg'

# Agent ###################################
t = Appearance("Agent Johnson")
t.colorTexture = "agentColor"
t.colorMaskTexture = "agentColorMask"
t.defaultColor = (0.3,0.3,0.33)
t.defaultHighlight = (1,0.5,0.3)
t.iconTexture = "agentIcon"
t.iconMaskTexture = "agentIconColorMask"
t.headModel =     "agentHead"
t.torsoModel =    "agentTorso"
t.pelvisModel =   "agentPelvis"
t.upperArmModel = "agentUpperArm"
t.foreArmModel =  "agentForeArm"
t.handModel =     "agentHand"
t.upperLegModel = "agentUpperLeg"
t.lowerLegModel = "agentLowerLeg"
t.toesModel =     "agentToes"
agentSounds =    ['agent1','agent2','agent3','agent4']
agentHitSounds = ['agentHit1','agentHit2']
t.attackSounds = agentSounds
t.jumpSounds = agentSounds
t.impactSounds = agentHitSounds
t.deathSounds=["agentDeath"]
t.pickupSounds = agentSounds
t.fallSounds=["agentFall"]
t.style = 'agent'

# Pixie ###################################
t = Appearance("Pixel")
t.colorTexture = "pixieColor"
t.colorMaskTexture = "pixieColorMask"
t.defaultColor = (0,1,0.7)
t.defaultHighlight = (0.65,0.35,0.75)
t.iconTexture = "pixieIcon"
t.iconMaskTexture = "pixieIconColorMask"
t.headModel =     "pixieHead"
t.torsoModel =    "pixieTorso"
t.pelvisModel =   "pixiePelvis"
t.upperArmModel = "pixieUpperArm"
t.foreArmModel =  "pixieForeArm"
t.handModel =     "pixieHand"
t.upperLegModel = "pixieUpperLeg"
t.lowerLegModel = "pixieLowerLeg"
t.toesModel =     "pixieToes"
pixieSounds =    ['pixie1','pixie2','pixie3','pixie4']
pixieHitSounds = ['pixieHit1','pixieHit2']
t.attackSounds = pixieSounds
t.jumpSounds = pixieSounds
t.impactSounds = pixieHitSounds
t.deathSounds=["pixieDeath"]
t.pickupSounds = pixieSounds
t.fallSounds=["pixieFall"]
t.style = 'pixie'

# Bunny ###################################
t = Appearance("Easter Bunny")
t.colorTexture = "bunnyColor"
t.colorMaskTexture = "bunnyColorMask"
t.defaultColor = (1,1,1)
t.defaultHighlight = (1,0.5,0.5)
t.iconTexture = "bunnyIcon"
t.iconMaskTexture = "bunnyIconColorMask"
t.headModel =     "bunnyHead"
t.torsoModel =    "bunnyTorso"
t.pelvisModel =   "bunnyPelvis"
t.upperArmModel = "bunnyUpperArm"
t.foreArmModel =  "bunnyForeArm"
t.handModel =     "bunnyHand"
t.upperLegModel = "bunnyUpperLeg"
t.lowerLegModel = "bunnyLowerLeg"
t.toesModel =     "bunnyToes"
bunnySounds =    ['bunny1','bunny2','bunny3','bunny4']
bunnyHitSounds = ['bunnyHit1','bunnyHit2']
t.attackSounds = bunnySounds
t.jumpSounds = ['bunnyJump']
t.impactSounds = bunnyHitSounds
t.deathSounds=["bunnyDeath"]
t.pickupSounds = bunnySounds
t.fallSounds=["bunnyFall"]
t.style = 'bunny'

# Ronnie ###################################
t = Appearance("Ronnie")
t.colorTexture = "ronnieColor"
t.colorMaskTexture = "ronnieColorMask"
t.defaultColor = (1,0.5,)
t.defaultHighlight = (1,1,1)
t.iconTexture = "ronnieIcon"
t.iconMaskTexture = "ronnieIconColorMask"
t.headModel =     "ronnieHead"
t.torsoModel =    "ronnieTorso"
t.pelvisModel =   "aliPelvis"
t.upperArmModel = "zero"
t.foreArmModel =  "zero"
t.handModel =     "ronnieHand"
t.upperLegModel = "zero"
t.lowerLegModel = "zero"
t.toesModel =     "ronnieToes"
ronnieSounds =    ['ronnie1','ronnie2','ronnie3','ronnie4','ronnie5','ronnie6','ronnie7']
ronnieHitSounds = ['ronniePain1','ronniePain2','ronniePain3','ronniePain4','ronniePain5']
t.attackSounds = ronnieSounds
t.jumpSounds = ronnieSounds
t.impactSounds = ronnieHitSounds
t.deathSounds=['ronnieDeath1','ronnieDeath2']
t.pickupSounds = ronnieSounds
t.fallSounds=["ronnieFall"]
t.style = 'ali'

##CUSTOM CHARACTERS BELOW
# Looie ###################################
t = Appearance("Looie")
t.colorTexture = "looieColor"
t.colorMaskTexture = "looieMask"
t.defaultColor = (1,0.7,0.0)
t.defaultHighlight = (1,1,1)
t.iconTexture = "looieIcon"
t.iconMaskTexture = "looieIconMask"
t.headModel =     "looieHead"
t.torsoModel =    "looieBody"
t.pelvisModel =   "aliPelvis"
t.upperArmModel = "zero"
t.foreArmModel =  "zero"
t.handModel =     "looieHand"
t.upperLegModel = "zero"
t.lowerLegModel = "looieLowerLeg"
t.toesModel =     "zero"
looieSounds =    ['looie1','looie2','looie3','looie4','looie5','looie6','looie7']
looieHitSounds = ['looiePain1','looiePain2','looiePain3','looiePain4','looiePain5']
t.attackSounds = looieSounds
t.jumpSounds = looieSounds
t.impactSounds = looieHitSounds
t.deathSounds=['looieDeath1','looieDeath2','looieDeath3']
t.pickupSounds = looieSounds
t.fallSounds=["looieFall1","looieFall2"]
t.style = 'agent'

# AVGN ###################################
t = Appearance("AVGN")
t.colorTexture = "avgnColor"
t.colorMaskTexture = "avgnColorMask"
t.defaultColor = (1,1,1)
t.defaultHighlight = (0.53,0.28,0.14)
t.iconTexture = "avgnIcon"
t.iconMaskTexture = "avgnIconColorMask"
t.headModel =     "agentHead"
t.torsoModel =    "agentTorso"
t.pelvisModel =   "agentPelvis"
t.upperArmModel = "agentUpperArm"
t.foreArmModel =  "agentForeArm"
t.handModel =     "agentHand"
t.upperLegModel = "agentUpperLeg"
t.lowerLegModel = "agentLowerLeg"
t.toesModel =     "agentToes"
agentSounds =    ['avgn1','avgn2','avgn3','avgn4']
agentHitSounds = ['avgnPain1','avgnPain2','avgnPain3']
t.attackSounds = agentSounds
t.jumpSounds = agentSounds
t.impactSounds = agentHitSounds
t.deathSounds=["avgnDeath1","avgnDeath2","avgnDeath3","avgnDeath4","avgnDeath5"]
t.pickupSounds = agentSounds
t.fallSounds=["avgnFall1","avgnFall2","avgnFall3"]
t.style = 'agent'

# Zill ###################################
t = Appearance("Zill")
t.colorTexture = "zillColor"
t.colorMaskTexture = "zillColorMask"
t.defaultColor = (0.1,1,0.1)
t.defaultHighlight = (1,1,0)
t.iconTexture = "zillIcon"
t.iconMaskTexture = "zillIconColorMask"
t.headModel =     "zillHead"
t.torsoModel =    "zillBody"
t.pelvisModel =   "zero"
t.upperArmModel = "zillUpperArm"
t.foreArmModel =  "zillForeArm"
t.handModel =     "zillHand"
t.upperLegModel = "zillUpperLeg"
t.lowerLegModel = "zillLowerLeg"
t.toesModel =     "zero"
t.attackSounds = ['zillAttack1','zillAttack2','zillAttack3','zillAttack4','zillAttack5']
t.jumpSounds = ['zillJump1','zillJump2','zillJump3','zillJump4']
t.impactSounds = ['zillPain1','zillPain2','zillPain3','zillPain4','zillPain5']
t.pickupSounds = ['zillPickup1','zillPickup2','zillPickup3','zillPickup4','zillPickup5']
t.deathSounds=['zillDeath1','zillDeath2','zillDeath3','zillDeath4']
t.fallSounds=["zillFall1","zillFall2"]
t.style = 'cyborg'

# Spy ###################################
t = Appearance("Spy")
t.colorTexture = "spyColor"
t.colorMaskTexture = "spyColorMask"
t.defaultColor = (1,1,1)
t.defaultHighlight = (0.1,0.1,0.1)
t.iconTexture = "spyIcon"
t.iconMaskTexture = "spyIconColorMask"
t.headModel =     "spyHead"
t.torsoModel =    "spyTorso"
t.pelvisModel =   "spyPelvis"
t.upperArmModel = "spyUpperArm"
t.foreArmModel =  "spyForeArm"
t.handModel =     "spyHand"
t.upperLegModel = "spyUpperLeg"
t.lowerLegModel = "spyLowerLeg"
t.toesModel =     "spyToes"
t.attackSounds = ['spyAttack1','spyAttack2','spyAttack3','spyAttack4']
t.jumpSounds = ['spyJump1','spyJump2','spyJump3','spyJump4','spyJump5']
t.impactSounds = ['spyPain1','spyPain2','spyPain3','spyPain4']
t.deathSounds=['spyDeath1','spyDeath2','spyDeath3','spyDeath4','spyDeath5']
t.pickupSounds = ['spyPickup1','spyPickup2']
t.fallSounds=["spyFall1"]
t.style = 'agent'

# Mictlan ###################################
t = Appearance("Mictlan")
t.colorTexture = "mictlanColor"
t.colorMaskTexture = "mictlanColorMask"
t.defaultColor = (0.1,1,1)
t.defaultHighlight = (0.1,0.1,0.1)
t.iconTexture = "mictlanIcon"
t.iconMaskTexture = "mictlanIconColorMask"
t.headModel =     "zero"
t.torsoModel =    "mictlanTorso"
t.pelvisModel =   "aliPelvis"
t.upperArmModel = "mictlanUpperArm"
t.foreArmModel =  "mictlanForeArm"
t.handModel =     "mictlanHand"
t.upperLegModel = "mictlanUpperLeg"
t.lowerLegModel = "mictlanLowerLeg"
t.toesModel =     "mictlanToes"
mictlanSounds =    ['mictlan1','mictlan2','mictlan3','mictlan4','mictlan5','mictlan6','mictlan7','mictlan8']
mictlanHitSounds = ['mictlanPain1','mictlanPain2','mictlanPain3']
t.attackSounds = mictlanSounds
t.jumpSounds = mictlanSounds
t.impactSounds = mictlanHitSounds
t.deathSounds=["mictlanDeath"]
t.pickupSounds = mictlanSounds
t.fallSounds=["mictlanFall"]
t.style = 'agent'

# Wizard ###################################
t = Appearance("Grumbledorf")
t.colorTexture = "wizardColor"
t.colorMaskTexture = "wizardColorMask"
t.defaultColor = (0.5,0.25,1.0)
t.defaultHighlight = (1,1,0)
t.iconTexture = "wizardIcon"
t.iconMaskTexture = "wizardIconColorMask"
t.headModel =     "wizardHead"
t.torsoModel =    "wizardTorso"
t.pelvisModel =   "wizardPelvis"
t.upperArmModel = "wizardUpperArm"
t.foreArmModel =  "wizardForeArm"
t.handModel =     "wizardHand"
t.upperLegModel = "wizardUpperLeg"
t.lowerLegModel = "wizardLowerLeg"
t.toesModel =     "wizardToes"
wizardSounds =    ['wizard1','wizard2','wizard3','wizard4','wizard5']
wizardHitSounds = ['wizardPain1','wizardPain2','wizardPain3']
t.attackSounds = wizardSounds
t.jumpSounds = wizardSounds
t.impactSounds = wizardHitSounds
t.deathSounds=["wizardDeath1","wizardDeath2","wizardDeath3","wizardDeath4",]
t.pickupSounds = ['wizardPickup1','wizardPickup2']
t.fallSounds=["wizardFall"]
t.style = 'agent'

# Milk (Cow Character) ###################################
t = Appearance("Milk")
t.colorTexture = "cowColor"
t.colorMaskTexture = "cowColorMask"
t.defaultColor = (1,1,1)
t.defaultHighlight = (1,0.3,0.5)
t.iconTexture = "cowIcon"
t.iconMaskTexture = "cowIconColorMask"
t.headModel =     "cowHead"
t.torsoModel =    "cowTorso"
t.pelvisModel =   "cowPelvis"
t.upperArmModel = "cowUpperArm"
t.foreArmModel =  "cowForeArm"
t.handModel =     "cowHand"
t.upperLegModel = "cowUpperLeg"
t.lowerLegModel = "cowLowerLeg"
t.toesModel =     "cowToes"
cowSounds =    ['cow1','cow2','cow3','cow4']
t.attackSounds = cowSounds
t.jumpSounds = cowSounds
t.impactSounds = cowSounds
t.deathSounds = ["cowDeath"]
t.pickupSounds = cowSounds
t.fallSounds = ["cowFall"]
t.style = 'bear'

# JuiceBoy ###################################
t = Appearance("Juice-Boy")
t.colorTexture = "juiceBoyColor"
t.colorMaskTexture = "juiceBoyColorMask"
t.defaultColor = (0.2,1,0.2)
t.defaultHighlight = (1,1,0)
t.iconTexture = "juiceBoyIcon"
t.iconMaskTexture = "juiceBoyIconColorMask"
t.headModel =     "zero"
t.torsoModel =    "juiceBoyTorso"
t.pelvisModel =   "zero"
t.upperArmModel = "juiceBoyUpperArm"
t.foreArmModel =  "juiceBoyForeArm"
t.handModel =     "juiceBoyHand"
t.upperLegModel = "juiceBoyUpperLeg"
t.lowerLegModel = "juiceBoyLowerLeg"
t.toesModel =     "juiceBoyToes"
juiceSounds = ['juice1','juice2','juice3','juice4','juice5','juice6']
t.attackSounds = juiceSounds
t.jumpSounds = juiceSounds
t.impactSounds = juiceSounds
t.deathSounds = ["juiceDeath"]
t.pickupSounds = juiceSounds
t.fallSounds = ["juiceFall"]
t.style = 'agent'

# Klayman - WORK IN PROGRESS###################################
'''
t = Appearance("Klayman")
t.colorTexture = "agentColor"
t.colorMaskTexture = "agentColorMask"
t.defaultColor = (1,0.1,0.1)
t.defaultHighlight = (1,0.7,0.0)
t.iconTexture = "klaymanIcon"
t.iconMaskTexture = "klaymanIconColorMask"
t.headModel =     "agentHead"
t.torsoModel =    "agentTorso"
t.pelvisModel =   "agentPelvis"
t.upperArmModel = "agentUpperArm"
t.foreArmModel =  "agentForeArm"
t.handModel =     "agentHand"
t.upperLegModel = "agentUpperLeg"
t.lowerLegModel = "agentLowerLeg"
t.toesModel =     "agentToes"
agentSounds =    ['agent1','agent2','agent3','agent4']
agentHitSounds = ['agentHit1','agentHit2']
t.attackSounds = agentSounds
t.jumpSounds = agentSounds
t.impactSounds = agentHitSounds
t.deathSounds=["agentDeath"]
t.pickupSounds = agentSounds
t.fallSounds=["agentFall"]
t.style = 'agent'
'''