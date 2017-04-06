import bs
import random


defaultPowerupInterval = 8000
coopPowerupDropRate = 3000

class PowerupMessage(object):
    """
    category: Message Classes

    Tell something to get a powerup.
    This message is normally recieved by touching
    a bs.Powerup box.
    
    Attributes:
    
       powerupType
          The type of powerup to be granted (a string). See bs.Powerup.powerupType for available type values.

       sourceNode
          The node the powerup game from, or an empty bs.Node ref otherwise.
          If a powerup is accepted, a bs.PowerupAcceptMessage should be sent
          back to the sourceNode to inform it of the fact. This will generally
          cause the powerup box to make a sound and disappear or whatnot.
    """
    def __init__(self,powerupType,sourceNode=bs.Node(None)):
        """
        Instantiate with given values.
        See bs.Powerup.powerupType for available type values.
        """
        self.powerupType = powerupType
        self.sourceNode = sourceNode

class PowerupAcceptMessage(object):
    """
    category: Message Classes

    Inform a bs.Powerup that it was accepted.
    This is generally sent in response to a bs.PowerupMessage
    to inform the box (or whoever granted it) that it can go away.
    """
    pass

class _TouchedMessage(object):
    pass

class PowerupFactory(object):
    """
    category: Game Flow Classes
    
    Wraps up media and other resources used by bs.Powerups.
    A single instance of this is shared between all powerups
    and can be retrieved via bs.Powerup.getFactory().

    Attributes:

       model
          The bs.Model of the powerup box.

       modelSimple
          A simpler bs.Model of the powerup box, for use in shadows, etc.

       texBox
          Triple-bomb powerup bs.Texture.

       texPunch
          Punch powerup bs.Texture.

       texIceBombs
          Ice bomb powerup bs.Texture.

       texStickyBombs
          Sticky bomb powerup bs.Texture.

       texShield
          Shield powerup bs.Texture.

       texImpactBombs
          Impact-bomb powerup bs.Texture.

       texHealth
          Health powerup bs.Texture.

       texLandMines
          Land-mine powerup bs.Texture.

       texCurse
          Curse powerup bs.Texture.

       healthPowerupSound
          bs.Sound played when a health powerup is accepted.

       powerupSound
          bs.Sound played when a powerup is accepted.

       powerdownSound
          bs.Sound that can be used when powerups wear off.

       powerupMaterial
          bs.Material applied to powerup boxes.

       powerupAcceptMaterial
          Powerups will send a bs.PowerupMessage to anything they touch
          that has this bs.Material applied.
    """

    def __init__(self):
        """
        Instantiate a PowerupFactory.
        You shouldn't need to do this; call bs.Powerup.getFactory() to get a shared instance.
        """

        self._lastPowerupType = None

        self.model = bs.getModel("powerup")
        self.modelSimple = bs.getModel("powerupSimple")

        self.texBomb = bs.getTexture("powerupBomb")
        self.texPunch = bs.getTexture("powerupPunch")
        self.texIceBombs = bs.getTexture("powerupIceBombs")
        self.texStickyBombs = bs.getTexture("powerupStickyBombs")
        self.texShield = bs.getTexture("powerupShield")
        self.texImpactBombs = bs.getTexture("powerupImpactBombs")
        self.texHealth = bs.getTexture("powerupHealth")
        self.texLandMines = bs.getTexture("powerupLandMines")
        self.texRangerBombs = bs.getTexture("powerupRangerBombs")
        self.texCombatBombs = bs.getTexture("powerupCombatBombs")
        self.texFireBombs = bs.getTexture("powerupFireBombs")
        self.texDynamitePack = bs.getTexture("powerupDynamitePack")
        self.texGrenades = bs.getTexture("powerupGrenade")
        self.texHealBombs = bs.getTexture("powerupHealBombs")
        self.texKnockerBombs = bs.getTexture("powerupKnockerBombs")
        self.texCurse = bs.getTexture("powerupCurse")
        self.texOverdrive = bs.getTexture("powerupOverdrive")
        self.texHijump = bs.getTexture("powerupHijump")
        self.texSpeed = bs.getTexture("powerupSpeed")
        self.texBlast = bs.getTexture("powerupBlast")

        self.healthPowerupSound = bs.getSound("healthPowerup")
        self.overdrivePowerupSound = bs.getSound("overdrivePowerup")
        self.powerupSound = bs.getSound("powerup01")
        self.powerdownSound = bs.getSound("powerdown01")
        self.dropSound = bs.getSound("boxDrop")

        # material for powerups
        self.powerupMaterial = bs.Material()

        # material for anyone wanting to accept powerups
        self.powerupAcceptMaterial = bs.Material()

        # pass a powerup-touched message to applicable stuff
        self.powerupMaterial.addActions(
            conditions=(("theyHaveMaterial",self.powerupAcceptMaterial)),
            actions=(("modifyPartCollision","collide",True),
                     ("modifyPartCollision","physical",False),
                     ("message","ourNode","atConnect",_TouchedMessage())))

        # we dont wanna be picked up
        self.powerupMaterial.addActions(
            conditions=("theyHaveMaterial",bs.getSharedObject('pickupMaterial')),
            actions=( ("modifyPartCollision","collide",False)))

        self.powerupMaterial.addActions(
            conditions=("theyHaveMaterial",bs.getSharedObject('footingMaterial')),
            actions=(("impactSound",self.dropSound,0.5,0.1)))

        self._powerupDist = []
        for p,freq in getDefaultPowerupDistribution():
            for i in range(int(freq)):
                self._powerupDist.append(p)

    def getRandomPowerupType(self,forceType=None,excludeTypes=[]):
        """
        Returns a random powerup type (string).
        See bs.Powerup.powerupType for available type values.

        There are certain non-random aspects to this; a 'curse' powerup, for instance,
        is always followed by a 'health' powerup (to keep things interesting).
        Passing 'forceType' forces a given returned type while still properly interacting
        with the non-random aspects of the system (ie: forcing a 'curse' powerup will result
        in the next powerup being health).
        
        gameSpecificExcludeTypes include only the powerups that you don't want them in specific gamemodes where they
        are useless, like a Healing Bomb, why the hell would you want to heal enemies?
        """
        import weakref
        
        # Disable some powerups based on the gamemode
        self._gamemode = bs.getActivity().getName()
        self._map = bs.getActivity()._map.getName()
        if self._gamemode == 'Race' or self._gamemode == 'Assault' or self._gamemode == 'Capture The Flag' or self._gamemode == 'Basketball' or self._gamemode == 'Conquest' or self._gamemode == 'Hockey' or self._gamemode == 'Football' or self._map == 'Crag Castle' or self._map == 'Bacon Greece' or self._map == 'Zigzag' or self._map == 'A Space Odyssey' or self._map == 'Happy Thoughts': # Disable speed where completing the objective faster is essential
            speedDisable = ['speed']
        else:
            speedDisable = []
        if self._map == 'Lake Frigid' or self._map == 'Hockey Stadium' or self._map == 'Football Stadium' or self._map == 'Bridgit' or self._map == 'Monkey Face' or self._map == 'Doom Shroom Large' or self._map == 'Doom Shroom' or self._map == 'Tower D' or self._gamemode == 'Basketball' or self._map == 'Courtyard' or self._map == 'Rampage' or self._map == 'Toilet Donut' or self._map == 'OUYA' or self._map == 'Hovering Plank-o-Wood' or self._map == 'Courtyard Night' or self._map == 'Block Fortress' or self._map == 'Mush Feud' or self._map == 'Flapland' or self._map == 'A Space Odyssey' or self._map == 'Happy Thoughts' or isinstance(bs.getSession(),bs.CoopSession): # Disable hi-jump on flat maps and Coop
            hijumpDisable = ['hijump']
        else:
            hijumpDisable = []
        if bs.getConfig().get('Easy Mode', True): # If Easy Mode is enabled, disable the most difficult powerups
            nonHardMode=['hijump','speed','combatBombs','knockerBombs']
        else:
            nonHardMode=[]
        if isinstance(bs.getSession(),bs.FreeForAllSession): # Disable Healing Bombs in FFA games
            notFFA=['healBombs']
        else:
            notFFA=[]
        if forceType: t = forceType
        else:
            if isinstance(bs.getSession(),bs.FreeForAllSession): 
                self.healthPowerups = ['health']
            else:
                self.healthPowerups = ['health','healBombs']
            if bs.getConfig().get('Easy Mode',True): self.shieldCounters = ['grenades', 'impactBombs']
            else: self.shieldCounters = ['grenades', 'impactBombs', 'combatBombs']
            if self._lastPowerupType == 'curse': t = random.choice(self.healthPowerups)
            elif self._lastPowerupType == 'shield': 
                if not isinstance(bs.getSession(),bs.CoopSession): t = random.choice(self.shieldCounters)
            while True:
                t = self._powerupDist[random.randint(0,len(self._powerupDist)-1)]
                if t not in excludeTypes and t not in notFFA and t not in speedDisable and t not in hijumpDisable and t not in nonHardMode:
                    break
        self._lastPowerupType = t
        return t


def getDefaultPowerupDistribution():
    try: pd = bs.getConfig()['Powerup Distribution']
    except Exception: pd = 'JRMP'
    if not isinstance(bs.getSession(),bs.CoopSession):
        if (pd == 'JRMP'):
            return (('tripleBombs',2),
                    ('iceBombs',1),
                    ('punch',1),
                    ('impactBombs',3),
                    ('landMines',2),
                    ('stickyBombs',3),
                    ('combatBombs',3),
                    ('dynamitePack',2),
                    ('rangerBombs',2),
                    ('knockerBombs',2),
                    ('grenades',1),
                    ('blastBuff',2),
                    ('fireBombs',0),
                    ('healBombs',1),
                    ('shield',1),
                    ('overdrive',1),
                    ('health',1),
                    ('curse',1),
                    ('hijump',1),
                    ('speed',1))
        if (pd == 'Classic'):
            return (('tripleBombs',3),
                    ('iceBombs',3),
                    ('punch',3),
                    ('impactBombs',3),
                    ('landMines',2),
                    ('stickyBombs',3),
                    ('shield',2),
                    ('health',1),
                    ('curse',1),
                    ('blastBuff',0),
                    ('overdrive',0),
                    ('combatBombs',0),
                    ('dynamitePack',0),
                    ('knockerBombs',0),
                    ('rangerBombs',0),
                    ('grenades',0),
                    ('fireBombs',0),
                    ('healBombs',0),
                    ('hijump',0),
                    ('speed',0))
        if (pd == 'Competetive'):
            return (('tripleBombs',0),
                    ('iceBombs',1),
                    ('punch',0),
                    ('impactBombs',1),
                    ('landMines',1),
                    ('stickyBombs',1),
                    ('combatBombs',1),
                    ('dynamitePack',1),
                    ('rangerBombs',1),
                    ('grenades',0),
                    ('knockerBombs',1),
                    ('blastBuff',0),
                    ('fireBombs',0),
                    ('healBombs',1),
                    ('shield',0),
                    ('overdrive',0),
                    ('health',0),
                    ('curse',0),
                    ('hijump',1),
                    ('speed',0))
        if (pd == 'No Powerups'):
            return (('tripleBombs',0),
                    ('iceBombs',0),
                    ('punch',0),
                    ('impactBombs',0),
                    ('landMines',0),
                    ('stickyBombs',0),
                    ('combatBombs',0),
                    ('dynamitePack',0),
                    ('rangerBombs',0),
                    ('grenades',0),
                    ('fireBombs',0),
                    ('healBombs',0),
                    ('knockerBombs',0),
                    ('shield',0),
                    ('overdrive',0),
                    ('blastBuff',0),
                    ('health',0),
                    ('curse',0),
                    ('hijump',0),
                    ('speed',0))
    else:
        return (('tripleBombs',2),
                ('iceBombs',2),
                ('punch',1),
                ('impactBombs',3),
                ('landMines',2),
                ('stickyBombs',3),
                ('combatBombs',3),
                ('dynamitePack',2),
                ('rangerBombs',1),
                ('grenades',1),
                ('blastBuff',2),
                ('fireBombs',0),
                ('healBombs',1),
                ('knockerBombs',0),
                ('shield',1),
                ('overdrive',1),
                ('health',1),
                ('curse',0),
                ('hijump',0),
                ('speed',1))
                    
class Powerup(bs.Actor):
    """
    category: Game Flow Classes

    A powerup box.
    This will deliver a bs.PowerupMessage to anything that touches it
    which has the bs.PowerupFactory.powerupAcceptMaterial applied.

    Attributes:

       powerupType
          The string powerup type.  This can be 'tripleBombs', 'punch',
          'iceBombs', 'impactBombs', 'landMines', 'stickyBombs', 'shield',
          'health', or 'curse'.

       node
          The 'prop' bs.Node representing this box.
    """

    def __init__(self,position=(0,1,0),powerupType='tripleBombs',expire=True):
        """
        Create a powerup-box of the requested type at the requested position.

        see bs.Powerup.powerupType for valid type strings.
        """
        
        bs.Actor.__init__(self)

        factory = self.getFactory()
        self.powerupType = powerupType;
        self._powersGiven = False

        if powerupType == 'tripleBombs': tex = factory.texBomb
        elif powerupType == 'punch': tex = factory.texPunch
        elif powerupType == 'iceBombs': tex = factory.texIceBombs
        elif powerupType == 'impactBombs': tex = factory.texImpactBombs
        elif powerupType == 'landMines': tex = factory.texLandMines
        elif powerupType == 'stickyBombs': tex = factory.texStickyBombs
        elif powerupType == 'rangerBombs': tex = factory.texRangerBombs
        elif powerupType == 'combatBombs': tex = factory.texCombatBombs
        elif powerupType == 'fireBombs': tex = factory.texFireBombs
        elif powerupType == 'dynamitePack': tex = factory.texDynamitePack
        elif powerupType == 'grenades': tex = factory.texGrenades
        elif powerupType == 'healBombs': tex = factory.texHealBombs
        elif powerupType == 'knockerBombs': tex = factory.texKnockerBombs
        elif powerupType == 'shield': tex = factory.texShield
        elif powerupType == 'health': tex = factory.texHealth
        elif powerupType == 'overdrive': tex = factory.texOverdrive
        elif powerupType == 'curse': tex = factory.texCurse
        elif powerupType == 'hijump': tex = factory.texHijump
        elif powerupType == 'speed': tex = factory.texSpeed
        elif powerupType == 'blastBuff': tex = factory.texBlast
        
        else: raise Exception("invalid powerupType: "+str(powerupType))

        if len(position) != 3: raise Exception("expected 3 floats for position")
        
        self.node = bs.newNode('prop',
                               delegate=self,
                               attrs={'body':'box',
                                      'position':position,
                                      'model':factory.model,
                                      'lightModel':factory.modelSimple,
                                      'shadowSize':0.5,
                                      'colorTexture':tex,
                                      'reflection':'powerup',
                                      'reflectionScale':[0.5],
                                      'materials':(factory.powerupMaterial,bs.getSharedObject('objectMaterial'))})

        # animate in..
        curve = bs.animate(self.node,"modelScale",{0:0,140:1.6,200:1})
        bs.gameTimer(200,curve.delete)

        if expire:
            bs.gameTimer(defaultPowerupInterval-2500,bs.WeakCall(self._startFlashing))
            bs.gameTimer(defaultPowerupInterval-1000,bs.WeakCall(self.handleMessage,bs.DieMessage()))

    @classmethod
    def getFactory(cls):
        """
        Returns a shared bs.PowerupFactory object, creating it if necessary.
        """
        activity = bs.getActivity()
        if activity is None: raise Exception("no current activity")
        try: return activity._sharedPowerupFactory
        except Exception:
            f = activity._sharedPowerupFactory = PowerupFactory()
            return f
            
    def _startFlashing(self):
        if self.node.exists(): self.node.flashing = True

        
    def handleMessage(self,m):
        self._handleMessageSanityCheck()

        if isinstance(m,PowerupAcceptMessage):
            factory = self.getFactory()
            if self.powerupType == 'health':
                bs.playSound(factory.healthPowerupSound,3,position=self.node.position)
            if self.powerupType == 'overdrive':
                bs.playSound(factory.overdrivePowerupSound,3,position=self.node.position)
            bs.playSound(factory.powerupSound,3,position=self.node.position)
            self._powersGiven = True
            self.handleMessage(bs.DieMessage())

        elif isinstance(m,_TouchedMessage):
            if not self._powersGiven:
                node = bs.getCollisionInfo("opposingNode")
                if node.exists(): node.handleMessage(PowerupMessage(self.powerupType,sourceNode=self.node))

        elif isinstance(m,bs.DieMessage):
            if self.node.exists():
                if (m.immediate):
                    self.node.delete()
                else:
                    curve = bs.animate(self.node,"modelScale",{0:1,100:0})
                    bs.gameTimer(100,self.node.delete)

        elif isinstance(m,bs.OutOfBoundsMessage):
            self.handleMessage(bs.DieMessage())

        elif isinstance(m,bs.HitMessage):
            # dont die on punches, hi-jump propel blasts and healing bomb blasts (thats annoying)
            if m.hitType != 'punch' and m.hitSubType != 'hijump' and m.hitSubType != 'healing' and m.hitSubType != 'knocker':
                self.handleMessage(bs.DieMessage())
        else:
            bs.Actor.handleMessage(self,m)
