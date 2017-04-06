import bs
import bsUtils
from bsVector import Vector
import random
import weakref


class BombFactory(object):
    """
    category: Game Flow Classes

    Wraps up media and other resources used by bs.Bombs
    A single instance of this is shared between all bombs
    and can be retrieved via bs.Bomb.getFactory().

    Attributes:

       bombModel
          The bs.Model of a standard or ice bomb.

       stickyBombModel
          The bs.Model of a sticky-bomb.

       impactBombModel
          The bs.Model of an impact-bomb.

       landMinModel
          The bs.Model of a land-mine.

       tntModel
          The bs.Model of a tnt box.

       regularTex
          The bs.Texture for regular bombs.

       iceTex
          The bs.Texture for ice bombs.

       stickyTex
          The bs.Texture for sticky bombs.

       impactTex
          The bs.Texture for impact bombs.

       impactLitTex
          The bs.Texture for impact bombs with lights lit.

       landMineTex
          The bs.Texture for land-mines.

       landMineLitTex
          The bs.Texture for land-mines with the light lit.

       tntTex
          The bs.Texture for tnt boxes.

       hissSound
          The bs.Sound for the hiss sound an ice bomb makes.

       debrisFallSound
          The bs.Sound for random falling debris after an explosion.

       woodDebrisFallSound
          A bs.Sound for random wood debris falling after an explosion.

       explodeSounds
          A tuple of bs.Sounds for explosions.

       freezeSound
          A bs.Sound of an ice bomb freezing something.

       fuseSound
          A bs.Sound of a burning fuse.

       activateSound
          A bs.Sound for an activating impact bomb.

       warnSound
          A bs.Sound for an impact bomb about to explode due to time-out.

       bombMaterial
          A bs.Material applied to all bombs.

       normalSoundMaterial
          A bs.Material that generates standard bomb noises on impacts, etc.

       stickyMaterial
          A bs.Material that makes 'splat' sounds and makes collisions softer.

       landMineNoExplodeMaterial
          A bs.Material that keeps land-mines from blowing up.
          Applied to land-mines when they are created to allow land-mines to
          touch without exploding.

       landMineBlastMaterial
          A bs.Material applied to activated land-mines that causes them to exlode on impact.

       impactBlastMaterial
          A bs.Material applied to activated impact-bombs that causes them to exlode on impact.

       blastMaterial
          A bs.Material applied to bomb blast geometry which triggers impact events with what it touches.

       dinkSounds
          A tuple of bs.Sounds for when bombs hit the ground.

       stickyImpactSound
          The bs.Sound for a squish made by a sticky bomb hitting something.

       rollSound
          bs.Sound for a rolling bomb.
    """

    def getRandomExplodeSound(self):
        'Return a random explosion bs.Sound from the factory.'
        return self.explodeSounds[random.randrange(len(self.explodeSounds))]
        
    def getRandomGrenadeSound(self):
        'Return a random explosion bs.Sound from the factory.'
        return self.grenadeExplodeSounds[random.randrange(len(self.grenadeExplodeSounds))]
        
    def getRandomTNTExplodeSound(self):
        'Return a random explosion bs.Sound from the factory.'
        return self.tntSounds[random.randrange(len(self.tntSounds))]

    def __init__(self):
        """
        Instantiate a BombFactory.
        You shouldn't need to do this; call bs.Bomb.getFactory() to get a shared instance.
        """

        self.bombModel = bs.getModel('bomb')
        self.stickyBombModel = bs.getModel('bombSticky')
        self.impactBombModel = bs.getModel('impactBomb')
        self.landMineModel = bs.getModel('landMine')
        self.combatBombModel = bs.getModel('combatBomb')
        self.tntModel = bs.getModel('tnt')
        self.miniDynamiteModel = bs.getModel('miniDynamite')
        self.crystalModel = bs.getModel('bombRanger')
        self.dynamiteModel = bs.getModel('dynamitePack')
        self.healingBombModel = bs.getModel('bombHealing')
        self.grenadeBombModel = bs.getModel('bombGrenade')
        self.basketballModel = bs.getModel('bombBasketball')
        self.knockerBombModel = bs.getModel('bombKnocker')
        
        self.regularTex = bs.getTexture('bombColor')
        self.iceTex = bs.getTexture('bombColorIce')
        self.rangerTex = bs.getTexture('bombRangerColor')
        self.stickyTex = bs.getTexture('bombStickyColor')
        self.fireTex = bs.getTexture('bombFireColor')
        self.combatTex = bs.getTexture('bombCombatColor')
        self.combatLitTex = bs.getTexture('bombCombatLitColor')
        self.impactTex = bs.getTexture('impactBombColor')
        self.impactLitTex = bs.getTexture('impactBombColorLit')
        self.healingTex = bs.getTexture('bombHealingColor')
        self.landMineTex = bs.getTexture('landMine')
        self.landMineLitTex = bs.getTexture('landMineLit')
        self.tntTex = bs.getTexture('tnt')
        self.dynamiteTex = bs.getTexture('dynamitePackTex')
        self.basketballTex = bs.getTexture('bombBasketballColor')
        self.knockerTex = bs.getTexture('bombKnockerColor')
        
        # Grenade Textres
        self.grenade3Tex = bs.getTexture('grenadeColor3') # 3 second fuse
        self.grenade2Tex = bs.getTexture('grenadeColor2') # 2 second fuse
        self.grenade1Tex = bs.getTexture('grenadeColor1') # 1 second fuse
        self.grenadeExTex = bs.getTexture('grenadeColorEx') # Just before explosion

        self.healingSound = bs.getSound('healingExplosion')
        self.hissSound = bs.getSound('hiss')
        self.crystalExplosionSound = bs.getSound('crystalExplosion')
        self.overdriveExplosionSound = bs.getSound('overdriveExplosion')
        self.debrisFallSound = bs.getSound('debrisFall')
        self.woodDebrisFallSound = bs.getSound('woodDebrisFall')
        self.pinOutSound = bs.getSound('grenadePinOut')
        self.hijumpSound = bs.getSound('hijump')
        self.dynamiteFuseSound = bs.getSound('fuseDynamite')
        
        # Combat Bomb sounds
        self.combatBombDeployedSound = bs.getSound('combatBombDeployed')
        self.combatBombReadySound = bs.getSound('combatBombReady')
        self.combatExplosionSound = bs.getSound('combatBombExplosion')
        
        # Grenade Explosions
        self.grenadeExplodeSounds = (bs.getSound('grenadeExplosion01'),
                              bs.getSound('grenadeExplosion02'),
                              bs.getSound('grenadeExplosion03'))

        self.explodeSounds = (bs.getSound('explosion01'),
                              bs.getSound('explosion02'),
                              bs.getSound('explosion03'),
                              bs.getSound('explosion04'),
                              bs.getSound('explosion05'))
                              
        self.knockerExplosionSound = bs.getSound('knockerExplosion')
                              
        self.tntSounds = (bs.getSound('tntExplode1'),
                              bs.getSound('tntExplode2'),
                              bs.getSound('tntExplode3'))

        self.freezeSound = bs.getSound('freeze')
        self.fireSound = bs.getSound('fire')
        self.fuseSound = bs.getSound('fuse01')
        self.activateSound = bs.getSound('activateBeep')
        self.warnSound = bs.getSound('warnBeep')

        # set up our material so new bombs dont collide with objects
        # that they are initially overlapping
        self.bombMaterial = bs.Material()
        self.normalSoundMaterial = bs.Material()
        self.crystalSoundMaterial = bs.Material()
        self.basketballSoundMaterial = bs.Material()
        self.stickyMaterial = bs.Material()

        self.bombMaterial.addActions(
            conditions=((('weAreYoungerThan',100),'or',('theyAreYoungerThan',100)),
                        'and',('theyHaveMaterial',bs.getSharedObject('objectMaterial'))),
            actions=(('modifyNodeCollision','collide',False)))

        # we want pickup materials to always hit us even if we're currently not
        # colliding with their node (generally due to the above rule)
        self.bombMaterial.addActions(
            conditions=('theyHaveMaterial',bs.getSharedObject('pickupMaterial')),
            actions=(('modifyPartCollision','useNodeCollide',False)))
        
        self.bombMaterial.addActions(actions=('modifyPartCollision','friction',0.3))

        self.landMineNoExplodeMaterial = bs.Material()
        self.landMineBlastMaterial = bs.Material()
        self.landMineBlastMaterial.addActions(
            conditions=(('weAreOlderThan',200),
                        'and',('theyAreOlderThan',200),
                        'and',('evalColliding',),
                        'and',(('theyDontHaveMaterial',self.landMineNoExplodeMaterial),
                               'and',(('theyHaveMaterial',bs.getSharedObject('objectMaterial')),
                                      'or',('theyHaveMaterial',bs.getSharedObject('playerMaterial'))))),
            actions=(('message','ourNode','atConnect',ImpactMessage())))

        
        self.impactBlastMaterial = bs.Material()
        self.impactBlastMaterial.addActions(
            conditions=(('weAreOlderThan',200),
                        'and',('theyAreOlderThan',200),
                        'and',('evalColliding',),
                        'and',(('theyHaveMaterial',bs.getSharedObject('footingMaterial')),
                               'or',('theyHaveMaterial',bs.getSharedObject('objectMaterial')))),
            actions=(('message','ourNode','atConnect',ImpactMessage())))
        

        self.blastMaterial = bs.Material()
        self.blastMaterial.addActions(
            conditions=(('theyHaveMaterial',bs.getSharedObject('objectMaterial'))),
            actions=(('modifyPartCollision','collide',True),
                     ('modifyPartCollision','physical',False),
                     ('message','ourNode','atConnect',ExplodeHitMessage())))

        self.dinkSounds = (bs.getSound('bombDrop01'),
                           bs.getSound('bombDrop02'))
        self.crystalDinkSound = (bs.getSound('crystalHit'))
        self.basketballHitSound = (bs.getSound('basketballHit'))
        self.stickyImpactSound = bs.getSound('stickyImpact')
        self.stickyImpactPlayerSound = bs.getSound('stickyImpactPlayer')
        

        self.rollSound = bs.getSound('bombRoll01')

        # collision sounds
        self.normalSoundMaterial.addActions(
            conditions=('theyHaveMaterial',bs.getSharedObject('footingMaterial')),
            actions=(('impactSound',self.dinkSounds,2,0.8),
                     ('rollSound',self.rollSound,3,6)))
                     
        self.crystalSoundMaterial.addActions(
            conditions=('theyHaveMaterial',bs.getSharedObject('footingMaterial')),
            actions=(('impactSound',self.crystalDinkSound,2,0.8),
                     ('rollSound',self.rollSound,3,6)))
                     
        self.basketballSoundMaterial.addActions(
            conditions=('theyHaveMaterial',bs.getSharedObject('footingMaterial')),
            actions=(('impactSound',self.basketballHitSound,2,0.8),
                     ('rollSound',self.rollSound,0,0)))

        self.stickyMaterial.addActions(
            actions=(('modifyPartCollision','stiffness',0.1),
                     ('modifyPartCollision','damping',1.0)))

        self.stickyMaterial.addActions(
            conditions=(('theyHaveMaterial',bs.getSharedObject('playerMaterial')),'or',('theyHaveMaterial',bs.getSharedObject('footingMaterial'))),
            actions=(('message','ourNode','atConnect',SplatMessage()))) 
        

class SplatMessage(object):
    pass

class ExplodeMessage(object):
    pass

class ImpactMessage(object):
    """ impact bomb touched something """
    pass

class ArmMessage(object):
    pass

class WarnMessage(object):
    pass
    
class DeployMessage(object):
    """ combat bomb is pulled out """
    pass

class ReadyMessage(object):
    """ combat bomb is about to explode """
    pass
    
class HealMessage(object):
    """ removes bombs without destroying them (works in collaboration with a Healing Bomb) """
    pass

class ExplodeHitMessage(object):
    "Message saying an object was hit"
    def __init__(self):
        pass

class Blast(bs.Actor):
    """
    category: Game Flow Classes

    An explosion, as generated by a bs.Bomb.
    """
    def __init__(self,position=(0,1,0),velocity=(0,0,0),blastRadius=2.0,blastType="normal",sourcePlayer=None,hitType='explosion',hitSubType='normal'):
        """
        Instantiate with given values.
        """
        bs.Actor.__init__(self)

        
        factory = Bomb.getFactory()

        self.blastType = blastType
        self.sourcePlayer = sourcePlayer

        self.hitType = hitType;
        self.hitSubType = hitSubType;

        # blast radius
        self.radius = blastRadius
        
        if self.hitSubType == 'knocker':
            self.node = bs.newNode('region',
                               attrs={'position':(position[0],position[1]-0.5,position[2]), # move down a bit so we throw more stuff upward
                                      'scale':(self.radius,self.radius+0.25,self.radius),
                                      'type':'sphere',
                                      'materials':(factory.blastMaterial,bs.getSharedObject('attackMaterial'))},
                               delegate=self)
        else:
            self.node = bs.newNode('region',
                               attrs={'position':(position[0],position[1]-0.1,position[2]), # move down a bit so we throw more stuff upward
                                      'scale':(self.radius,self.radius,self.radius),
                                      'type':'sphere',
                                      'materials':(factory.blastMaterial,bs.getSharedObject('attackMaterial'))},
                               delegate=self)

        bs.gameTimer(50,self.node.delete)

        # throw in an explosion and flash````
        explosion = bs.newNode("explosion",
                               attrs={'position':position,
                                      'velocity':(velocity[0],max(-1.0,velocity[1]),velocity[2]),
                                      'radius':self.radius,
                                      'big':(self.blastType == 'tnt' or self.blastType == 'ranger' or self.blastType == 'grenade')})
        if self.blastType == "ice":
            explosion.color = (0,0.05,0.4)
            
        if self.blastType == "fire":
            explosion.color = (1.25,0.8,0.8)   
            
        if self.blastType == "ranger":
            explosion.color = (1,1,0)
            
        if self.blastType == "curse":
            explosion.color = (0.8,0.36,0.4)
            
        if self.blastType == "combat":
            explosion.color = (0,0,1)
            
        if self.blastType == "knocker":
            explosion.color = (0.2,0.2,0.6)
            
        if self.blastType == "tnt":
            explosion.color = (0,1,0)
            
        if self.blastType == "healing":
            explosion.color = (1,0,0.3)
            
        if self.blastType == "hijump":
            explosion.color = (1,0.01,0.95)

        if self.blastType != 'ice': bs.emitBGDynamics(position=position,velocity=velocity,count=int(1.0+random.random()*4),emitType='tendrils',tendrilType='thinSmoke')
        if self.blastType != 'combat' and self.blastType != 'knocker': bs.emitBGDynamics(position=position,velocity=velocity,count=int(4.0+random.random()*4),emitType='tendrils',tendrilType='ice' if self.blastType == 'ice' else 'smoke')
        bs.emitBGDynamics(position=position,emitType='distortion',spread=1.0 if self.blastType == 'tnt' else 2.0)

        # and emit some shrapnel..
        if self.blastType == 'ice':
            def _doEmit():
                bs.emitBGDynamics(position=position,velocity=velocity,count=30,spread=2.0,scale=0.4,chunkType='ice',emitType='stickers');
            bs.gameTimer(50,_doEmit) # looks better if we delay a bit


        elif self.blastType == 'sticky':
            def _doEmit():
                bs.emitBGDynamics(position=position,velocity=velocity,count=int(4.0+random.random()*8),spread=0.7,chunkType='slime');
                bs.emitBGDynamics(position=position,velocity=velocity,count=int(4.0+random.random()*8),scale=0.5, spread=0.7,chunkType='slime');
                bs.emitBGDynamics(position=position,velocity=velocity,count=15,scale=0.6,chunkType='slime',emitType='stickers');
                bs.emitBGDynamics(position=position,velocity=velocity,count=20,scale=0.7,chunkType='spark',emitType='stickers');
                bs.emitBGDynamics(position=position,velocity=velocity,count=int(6.0+random.random()*12),scale=0.8,spread=1.5,chunkType='spark');
            bs.gameTimer(50,_doEmit) # looks better if we delay a bit
            
        elif self.blastType == 'dynamite':
            def _doEmit():
                    bs.emitBGDynamics(position=position,velocity=velocity,count=int(4.0+random.random()*8),chunkType='rock');
                    bs.emitBGDynamics(position=position,velocity=velocity,count=int(4.0+random.random()*8),scale=0.8,chunkType='rock');
                    bs.emitBGDynamics(position=position,velocity=velocity,count=int(8.0+random.random()*20),scale=0.7,spread=1.5,chunkType='spark');
                    bs.emitBGDynamics(position=position,velocity=velocity,count=60,scale=1.0,spread=3.0,chunkType='spark',emitType='stickers');
            bs.gameTimer(50,_doEmit) # looks better if we delay a bit
            
        elif self.blastType == 'impact': # regular bomb shrapnel
            def _doEmit():
                bs.emitBGDynamics(position=position,velocity=velocity,count=int(4.0+random.random()*8),scale=0.8,chunkType='metal');
                bs.emitBGDynamics(position=position,velocity=velocity,count=int(4.0+random.random()*8),scale=0.4,chunkType='metal');
                bs.emitBGDynamics(position=position,velocity=velocity,count=20,scale=0.7,chunkType='spark',emitType='stickers');
                bs.emitBGDynamics(position=position,velocity=velocity,count=int(8.0+random.random()*15),scale=0.8,spread=1.5,chunkType='spark');
            bs.gameTimer(50,_doEmit) # looks better if we delay a bit
            
        elif self.blastType == 'combat': # regular bomb shrapnel
            def _doEmit():
                bs.emitBGDynamics(position=position,velocity=velocity,count=int(4.0+random.random()*15),scale=0.9,chunkType='metal');
                bs.emitBGDynamics(position=position,velocity=velocity,count=int(4.0+random.random()*15),scale=0.5,chunkType='metal');
                bs.emitBGDynamics(position=position,velocity=velocity,count=30,scale=0.7,chunkType='spark',emitType='stickers');
                bs.emitBGDynamics(position=position,velocity=velocity,count=int(8.0+random.random()*20),scale=0.7,spread=1.5,chunkType='spark');
                bs.emitBGDynamics(position=position,emitType='distortion',spread=1.0);
            bs.gameTimer(50,_doEmit) # looks better if we delay a bit
            
        elif self.blastType == 'knocker': # regular bomb shrapnel
            def _doEmit():
                bs.emitBGDynamics(position=position,velocity=velocity,count=int(4.0+random.random()*30),scale=0.5,chunkType='ice');
                bs.emitBGDynamics(position=position,velocity=velocity,count=15,scale=0.3,chunkType='spark',emitType='stickers');
                bs.emitBGDynamics(position=position,velocity=velocity,count=int(4.0+random.random()*8),emitType='tendrils',tendrilType='ice')
                bs.emitBGDynamics(position=position,emitType='distortion',spread=0.3);
            bs.gameTimer(50,_doEmit) # looks better if we delay a bit
            
        elif self.blastType == 'hijump': # regular bomb shrapnel
            def _doEmit():
                bs.emitBGDynamics(position=position,emitType='distortion',spread=2.0);
                bs.emitBGDynamics(position=position,velocity=velocity,count=15,scale=1.0,chunkType='spark',emitType='stickers');
                bs.emitBGDynamics(position=position,velocity=velocity,count=int(8.0+random.random()*20),scale=0.3,spread=3.0,chunkType='spark');
            bs.gameTimer(50,_doEmit) # looks better if we delay a bit
            
        elif self.blastType == 'healing': # regular bomb shrapnel
            def _doEmit():
                bs.emitBGDynamics(position=position,emitType='distortion',spread=1.5);
                bs.emitBGDynamics(position=position,emitType='distortion',spread=2.0);
                bs.emitBGDynamics(position=position,emitType='distortion',spread=1.0);
                bs.emitBGDynamics(position=position,velocity=velocity,count=30,scale=1.0,chunkType='spark',emitType='stickers');
                bs.emitBGDynamics(position=position,velocity=velocity,count=int(8.0+random.random()*20),scale=0.7,spread=1.5,chunkType='spark');
            bs.gameTimer(50,_doEmit) # looks better if we delay a bit
            
        elif self.blastType == 'ranger': # regular bomb shrapnel
            def _doEmit():
                bs.emitBGDynamics(position=position,velocity=velocity,count=int(4.0+random.random()*20),scale=1.5,chunkType='spark');
                bs.emitBGDynamics(position=position,velocity=velocity,count=int(4.0+random.random()*20),scale=1.2,chunkType='spark');
                bs.emitBGDynamics(position=position,velocity=velocity,count=50,scale=0.7,chunkType='spark',emitType='stickers');
                bs.emitBGDynamics(position=position,velocity=velocity,count=int(8.0+random.random()*45),scale=1.0,spread=3,chunkType='spark');
            bs.gameTimer(50,_doEmit)
            
        elif self.blastType == 'grenade': # regular bomb shrapnel
            def _doEmit():
                bs.emitBGDynamics(position=position,velocity=velocity,count=int(6.0+random.random()*15),scale=0.8,chunkType='rock');
                bs.emitBGDynamics(position=position,velocity=velocity,count=int(6.0+random.random()*30),scale=0.5,chunkType='rock');
            bs.gameTimer(50,_doEmit)

        else: # regular or land mine bomb shrapnel
            def _doEmit():
                if self.blastType != 'tnt' and self.blastType != 'miniDynamite':
                    bs.emitBGDynamics(position=position,velocity=velocity,count=int(4.0+random.random()*8),chunkType='rock');
                    bs.emitBGDynamics(position=position,velocity=velocity,count=int(4.0+random.random()*8),scale=0.5,chunkType='rock');
                if self.blastType != 'miniDynamite':
                    bs.emitBGDynamics(position=position,velocity=velocity,count=30,scale=1.0 if self.blastType=='tnt' else 0.7,chunkType='spark',emitType='stickers');
                    bs.emitBGDynamics(position=position,velocity=velocity,count=int(18.0+random.random()*20),scale=1.0 if self.blastType == 'tnt' else 0.8,spread=1.5,chunkType='spark');

                # tnt throws metal chunks
                if self.blastType == 'tnt':
                    def _emitSplinters():
                        bs.emitBGDynamics(position=position,velocity=velocity,count=int(35.0+random.random()*50),scale=1.5,spread=1,chunkType='metal');
                    bs.gameTimer(10,_emitSplinters)
                
                # every now and then do a sparky one
                if self.blastType == 'tnt' or random.random() < 0.1:
                    def _emitExtraSparks():
                        bs.emitBGDynamics(position=position,velocity=velocity,count=int(10.0+random.random()*35),scale=2.5,spread=0.5,chunkType='spark');
                    bs.gameTimer(20,_emitExtraSparks)
                        
            bs.gameTimer(50,_doEmit) # looks better if we delay a bit

        if self.blastType == 'tnt':
            light = bs.newNode('light',
                           attrs={'position':position,
                                  'color': (0.4,0.7,0.4),
                                  'volumeIntensityScale': 10.0})
        elif self.blastType == 'ranger':
            light = bs.newNode('light',
                           attrs={'position':position,
                                  'color': (1,1,1),
                                  'volumeIntensityScale': 100.0})
        elif self.blastType == 'curse':
            light = bs.newNode('light',
                           attrs={'position':position,
                                  'color': (0.8,0.36,0.4),
                                  'volumeIntensityScale': 50.0})
        elif self.blastType == 'combat':
            light = bs.newNode('light',
                           attrs={'position':position,
                                  'color': (0.2,0.69,0.9),
                                  'volumeIntensityScale': 50.0})
        elif self.blastType == 'healing':
            light = bs.newNode('light',
                           attrs={'position':position,
                                  'color': (1,0.73,1),                                  
                                  'volumeIntensityScale': 10.0})                      
        elif self.blastType == 'hijump':
            light = bs.newNode('light',
                           attrs={'position':position,
                                  'color': (1,0.05,0.95),                                  
                                  'volumeIntensityScale': 5.0})
        elif self.blastType == 'knocker':
            light = bs.newNode('light',
                           attrs={'position':position,
                                  'color': (0.0,0.0,1.0),
                                  'volumeIntensityScale': 5.0})
        else:
            light = bs.newNode('light',
                           attrs={'position':position,
                                  'color': (0.6,0.6,1.0) if self.blastType == 'ice' else (1,0.3,0.1),
                                  'volumeIntensityScale': 10.0})

        s = random.uniform(0.6,0.9)
        scorchRadius = lightRadius = self.radius
        if self.blastType == 'tnt':
            lightRadius *= 1.4
            scorchRadius *= 1.15
            s *= 3.0
        elif self.blastType == 'ranger':
            lightRadius *= 1.6
            s *= 2.0
        elif self.blastType == 'combat':
            lightRadius *= 0.5
            s *= 2.0
        elif self.blastType == 'miniDynamite':
            lightRadius *= 0.15
            s *= 1.0  

        iScale = 1.6
        bsUtils.animate(light,"intensity",{0:2.0*iScale, int(s*20):0.1*iScale, int(s*25):0.2*iScale, int(s*50):17.0*iScale, int(s*60):5.0*iScale, int(s*80):4.0*iScale, int(s*200):0.6*iScale, int(s*2000):0.00*iScale, int(s*3000):0.0})
        bsUtils.animate(light,"radius",{0:lightRadius*0.2, int(s*50):lightRadius*0.55, int(s*100):lightRadius*0.3, int(s*300):lightRadius*0.15, int(s*1000):lightRadius*0.05})
        bs.gameTimer(int(s*3000),light.delete)

        # make a scorch that fades over time
        scorch = bs.newNode('scorch',
                        attrs={'position':position,'size':scorchRadius*0.5,'big':(self.blastType == 'tnt' or self.blastType == 'ranger' or self.blastType == 'grenade')})
        if self.blastType == 'ice':
            scorch.color = (1,1,1.5)
            
        if self.blastType == 'fire':
            scorch.color = (1.25,0.95,0.95)
            
        if self.blastType == 'ranger':
            scorch.color = (2,2,2)
            
        if self.blastType == 'hijump':
            scorch.color = (0.7,0.05,0.65)
           
        if self.blastType == 'healing':
            scorch.color = (2,1.73,2)
            
        if self.blastType == 'tnt':
            scorch.color = (0.4,0.7,0.4)

        if self.blastType == 'fire':
            bsUtils.animate(scorch,"presence",{3000:2, 5000:1.5, 5150:0.5, 8000:0})
            bs.gameTimer(8000,scorch.delete)
        else:
            bsUtils.animate(scorch,"presence",{3000:1, 13000:0})
            bs.gameTimer(13000,scorch.delete)

        if self.blastType == 'ice':
            bs.playSound(factory.hissSound,position=light.position)
            
        if self.blastType == 'ranger':
            bs.playSound(factory.crystalExplosionSound,position=light.position)  
          
        if self.blastType == 'curse':
            bs.playSound(factory.overdriveExplosionSound,position=light.position)            
            
        p = light.position
        if self.blastType == 'combat':
            bs.playSound(factory.combatExplosionSound,position=p)
        elif self.blastType == 'knocker':
            bs.playSound(factory.knockerExplosionSound,position=p)
        elif self.blastType == 'grenade':
            bs.playSound(factory.getRandomGrenadeSound(),volume=1.0,position=p)  
        elif self.blastType == 'hijump':
            bs.playSound(factory.hijumpSound,volume=2.0,position=p)  
        else:
            if self.blastType != 'miniDynamite':
                bs.playSound(factory.getRandomExplodeSound(),volume=1.0,position=p)
                bs.playSound(factory.debrisFallSound,position=p)
        
        if isinstance(bs.getSession(),bs.CoopSession) or bs.getConfig().get('Camera Shake', True):
            if self.blastType == 'ranger':
                bs.shakeCamera(intensity=2.0)
            elif self.blastType == 'curse':
                bs.shakeCamera(intensity=3.5)
            elif self.blastType == 'grenade':
                bs.shakeCamera(intensity=1.5)
            elif self.blastType == 'fire':
                bs.shakeCamera(intensity=0.25)
            elif self.blastType == 'hijump':
                bs.shakeCamera(intensity=0.1)
            elif self.blastType == 'combat':
                bs.shakeCamera(intensity=0.5)
            elif self.blastType == 'knocker':
                bs.shakeCamera(intensity=0.75)
            else:
                if self.blastType != 'miniDynamite':
                    bs.shakeCamera(intensity=5.0 if self.blastType == 'tnt' else 1.0)

        # tnt is more epic..
        if self.blastType == 'tnt':
            bs.playSound(factory.getRandomTNTExplodeSound(),position=p)
            def _extraBoom():
                bs.playSound(factory.getRandomExplodeSound(),position=p)
            bs.gameTimer(250,_extraBoom)
            def _extraBoom2():
                bs.playSound(factory.getRandomTNTExplodeSound(),position=p)
            bs.gameTimer(500,_extraBoom2)
            def _extraDebrisSound():
                bs.playSound(factory.debrisFallSound,position=p)
                bs.playSound(factory.woodDebrisFallSound,position=p)
            bs.gameTimer(400,_extraDebrisSound)

    def handleMessage(self,m):
        self._handleMessageSanityCheck()
        
        if isinstance(m,bs.DieMessage):
            self.node.delete()

        elif isinstance(m,ExplodeHitMessage):
            node = bs.getCollisionInfo("opposingNode")
            if node is not None:
                t = self.node.position

                # new
                mag = 2000.0
                if self.blastType == 'ice': mag *= 0.5
                elif self.blastType == 'impact': mag *= 1.0
                elif self.blastType == 'fire': mag *= 0.15
                elif self.blastType == 'landMine': mag *= 2.5
                elif self.blastType == 'tnt': mag *= 2.0
                elif self.blastType == 'knocker': mag *= 1.5
                elif self.blastType == 'combat': mag *= 1.85
                elif self.blastType == 'dynamite': mag *= 0.65
                elif self.blastType == 'miniDynamite': mag *= 0.8
                elif self.blastType == 'ranger': mag *= 1.15
                elif self.blastType == 'grenade': mag *= 1.15
                elif self.blastType == 'curse': mag *= 1.2
                elif self.blastType == 'healing': mag *= 0.0
                elif self.blastType == 'hijump': mag *= 1.0

                node.handleMessage(bs.HitMessage(pos=t,
                                                    velocity=(0,0,0),
                                                    magnitude=mag,
                                                    hitType=self.hitType,
                                                    hitSubType=self.hitSubType,
                                                    radius=self.radius,
                                                    sourcePlayer=self.sourcePlayer))
                if self.blastType == "ice":
                    bs.playSound(Bomb.getFactory().freezeSound,10,position=t)
                    node.handleMessage(bs.FreezeMessage())   
                                     
                if self.blastType == "fire":
                    bs.playSound(Bomb.getFactory().fireSound,10,position=t)
                    
                if self.blastType == "healing":
                    bs.playSound(Bomb.getFactory().healingSound,6,position=t)
                    node.handleMessage(bs.HealMessage())
                    
        else:
            bs.Actor.handleMessage(self,m)

class Bomb(bs.Actor):
    """
    category: Game Flow Classes
    
    A bomb and its variants such as land-mines and tnt-boxes.
    """

    def __init__(self,position=(0,1,0),velocity=(0,0,0),bombType='normal',blastRadius=2.0,sourcePlayer=None,owner=None):
        """
        Create a new Bomb.
        
        bombType can be 'ice','impact','landMine','normal','sticky', 'ranger', or 'tnt'.
        Note that for impact or landMine bombs you have to call arm()
        before they will go off.
        """
        bs.Actor.__init__(self)

        factory = self.getFactory()

        if not bombType in ('ice','impact','landMine','normal','sticky','ranger','tnt','combat','knocker','dynamite','miniDynamite','fire','healing','curse','grenade','hijump','basketball'): raise Exception("invalid bomb type: " + bombType)
        self.bombType = bombType

        self._exploded = False

        if self.bombType == 'sticky': self._lastStickySoundTime = 0

        self.blastRadius = blastRadius
        if self.bombType == 'ice': self.blastRadius *= 1.1
        elif self.bombType == 'fire': self.blastRadius *= 1.1
        elif self.bombType == 'impact': self.blastRadius *= 0.7
        elif self.bombType == 'combat': self.blastRadius *= 0.85
        elif self.bombType == 'knocker': self.blastRadius *= 1.5
        elif self.bombType == 'dynamite': self.blastRadius *= 0.75
        elif self.bombType == 'miniDynamite': self.blastRadius *= 0.65
        elif self.bombType == 'landMine': self.blastRadius *= 0.7
        elif self.bombType == 'tnt': self.blastRadius *= 1.6
        elif self.bombType == 'ranger': self.blastRadius *= 1.8
        elif self.bombType == 'curse': self.blastRadius *= 2.1
        elif self.bombType == 'healing': self.blastRadius *= 1.2
        elif self.bombType == 'grenade': self.blastRadius *= 1.45
        elif self.bombType == 'hijump': self.blastRadius *= 0.75

        self._explodeCallbacks = []
        
        # the player this came from
        self.sourcePlayer = sourcePlayer

        # by default our hit type/subtype is our own, but we pick up types of whoever
        # sets us off so we know what caused a chain reaction
        self.hitType = 'explosion'
        self.hitSubType = self.bombType

        # if no owner was provided, use an unconnected node ref
        if owner is None: owner = bs.Node(None)

        # the node this came from
        self.owner = owner

        # adding footing-materials to things can screw up jumping and flying since players carrying those things
        # and thus touching footing objects will think they're on solid ground..
        # perhaps we don't wanna add this even in the tnt case?..
        if self.bombType == 'tnt':
            materials = (factory.bombMaterial, bs.getSharedObject('footingMaterial'), bs.getSharedObject('objectMaterial'))
        else:
            materials = (factory.bombMaterial, bs.getSharedObject('objectMaterial'))
            
        if self.bombType == 'impact' or self.bombType == 'healing': materials = materials + (factory.impactBlastMaterial,)
        elif self.bombType == 'landMine': materials = materials + (factory.landMineNoExplodeMaterial,)

        if self.bombType == 'sticky': materials = materials + (factory.stickyMaterial,)
        elif self.bombType == 'ranger': materials = materials + (factory.crystalSoundMaterial,)
        elif self.bombType == 'basketball': materials = materials + (factory.basketballSoundMaterial,)
        else: materials = materials + (factory.normalSoundMaterial,)

        if self.bombType == 'landMine':
            self.node = bs.newNode('prop',
                                   delegate=self,
                                   attrs={'position':position,
                                          'velocity':velocity,
                                          'model':factory.landMineModel,
                                          'lightModel':factory.landMineModel,
                                          'body':'landMine',
                                          'shadowSize':0.44,
                                          'colorTexture':factory.landMineTex,
                                          'reflection':'powerup',
                                          'reflectionScale':[1.0],
                                          'materials':materials})

        elif self.bombType == 'tnt':
            self.node = bs.newNode('prop',
                                   delegate=self,
                                   attrs={'position':position,
                                          'velocity':velocity,
                                          'model':factory.tntModel,
                                          'lightModel':factory.tntModel,
                                          'body':'crate',
                                          'shadowSize':0.5,
                                          'colorTexture':factory.tntTex,
                                          'reflection':'soft',
                                          'reflectionScale':[0.23],
                                          'materials':materials})
                                          
        elif self.bombType == 'miniDynamite':
            fuseTime = 1
            self.node = bs.newNode('prop',
                                   delegate=self,
                                   attrs={'position':position,
                                          'velocity':velocity,
                                          'model':factory.miniDynamiteModel,
                                          'lightModel':factory.miniDynamiteModel,
                                          'body':'crate',
                                          'shadowSize':0.1,
                                          'modelScale':1,
                                          'bodyScale':0.55,
                                          'colorTexture':factory.dynamiteTex,
                                          'reflection':'soft',
                                          'reflectionScale':[0.1],
                                          'materials':materials})
                                          
        elif self.bombType == 'impact':
            fuseTime = 10000
            self.node = bs.newNode('prop',
                                   delegate=self,
                                   attrs={'position':position,
                                          'velocity':velocity,
                                          'body':'sphere',
                                          'model':factory.impactBombModel,
                                          'shadowSize':0.3,
                                          'colorTexture':factory.impactTex,
                                          'reflection':'powerup',
                                          'reflectionScale':[1.5],
                                          'materials':materials})
            self.armTimer = bs.Timer(200,bs.WeakCall(self.handleMessage,ArmMessage()))
            self.warnTimer = bs.Timer(fuseTime-1700,bs.WeakCall(self.handleMessage,WarnMessage()))
        elif self.bombType == 'hijump':
            fuseTime = 1
            self.node = bs.newNode('prop',
                                   delegate=self,
                                   attrs={'position':position,
                                          'velocity':velocity,
                                          'body':'sphere',
                                          'model':factory.impactBombModel,
                                          'shadowSize':0.3,
                                          'colorTexture':factory.impactTex,
                                          'reflection':'powerup',
                                          'reflectionScale':[1.5],
                                          'materials':materials})
            
        elif self.bombType == 'healing':
            fuseTime = 5000
            self.node = bs.newNode('prop',
                                   delegate=self,
                                   attrs={'position':position,
                                          'velocity':velocity,
                                          'body':'sphere',
                                          'model':factory.healingBombModel,
                                          'shadowSize':0.3,
                                          'colorTexture':factory.healingTex,
                                          'reflection':'powerup',
                                          'reflectionScale':[1.8],
                                          'materials':materials})
            self.deployedTimer = bs.Timer(1,bs.WeakCall(self.handleMessage,DeployMessage()))    
            
        elif self.bombType == 'combat':
            fuseTime = 2000
            self.node = bs.newNode('prop',
                                   delegate=self,
                                   attrs={'position':position,
                                          'velocity':velocity,
                                          'model':factory.combatBombModel,
                                          'lightModel':factory.combatBombModel,
                                          'body':'sphere',
                                          'shadowSize':0.5,
                                          'colorTexture':factory.combatTex,
                                          'reflection':'powerup',
                                          'reflectionScale':[1.0],
                                          'materials':materials})
            self.deployedFirstTimer = bs.Timer(300,bs.WeakCall(self.handleMessage,DeployMessage()))
            self.deployedTimer = bs.Timer(1200,bs.WeakCall(self.handleMessage,DeployMessage()))
            self.readyTimer = bs.Timer(fuseTime-250,bs.WeakCall(self.handleMessage,ReadyMessage()))
            
        elif self.bombType == 'basketball':
            self.node = bs.newNode('prop',
                                   delegate=self,
                                   attrs={'position':position,
                                          'velocity':velocity,
                                          'model':factory.basketballModel,
                                          'lightModel':factory.basketballModel,
                                          'body':'sphere',
                                          'shadowSize':0.5,
                                          'colorTexture':factory.basketballTex,
                                          'reflection':'soft',
                                          'reflectionScale':[0.35],
                                          'materials':materials})
            
        elif self.bombType == 'grenade':
            fuseTime = 3000
            self.node = bs.newNode('prop',
                                   delegate=self,
                                   attrs={'position':position,
                                          'velocity':velocity,
                                          'model':factory.grenadeBombModel,
                                          'lightModel':factory.grenadeBombModel,
                                          'body':'sphere',
                                          'shadowSize':0.1,
                                          'colorTexture':factory.grenade3Tex,
                                          'reflection':'soft',
                                          'reflectionScale':[0.5],
                                          'materials':materials})
            self.deployedTimer = bs.Timer(1,bs.WeakCall(self.handleMessage,DeployMessage()))

        else:
            fuseTime = 3000
            if self.bombType == 'sticky':
                sticky = True
                model = factory.stickyBombModel
                rType = 'sharper'
                rScale = 1.8
            elif self.bombType == 'ranger':
                fuseTime = 4000
                sticky = False
                model = factory.crystalModel
                rType = 'sharper'
                rScale = 1.8
                self.deployedTimer = bs.Timer(1,bs.WeakCall(self.handleMessage,DeployMessage()))
            elif self.bombType == 'knocker':
                fuseTime = 3000
                sticky = False
                model = factory.knockerBombModel
                rType = 'powerup'
                rScale = 0.35
            elif self.bombType == 'dynamite':
                fuseTime = 3000
                sticky = False
                model = factory.dynamiteModel
                rType = 'sharper'
                rScale = 0.8
                self.deployedTimer = bs.Timer(1,bs.WeakCall(self.handleMessage,DeployMessage()))
            else:
                sticky = False
                model = factory.bombModel
                rType = 'sharper'
                rScale = 1.8
            if self.bombType == 'ice': tex = factory.iceTex
            elif self.bombType == 'sticky': tex = factory.stickyTex
            elif self.bombType == 'dynamite': tex = factory.dynamiteTex
            elif self.bombType == 'fire': tex = factory.fireTex
            elif self.bombType == 'ranger': tex = factory.rangerTex
            elif self.bombType == 'knocker': tex = factory.knockerTex
            elif self.bombType == 'basketball': tex = factory.basketballTex
            # Curse bomb doesn't exist, but it's only used for the explosion. I'm gonna add the texture anyway.
            else: tex = factory.regularTex
            self.node = bs.newNode('bomb',
                                   delegate=self,
                                   attrs={'position':position,
                                          'velocity':velocity,
                                          'model':model,
                                          'shadowSize':0.3,
                                          'colorTexture':tex,
                                          'sticky':sticky,
                                          'owner':owner,
                                          'reflection':rType,
                                          'reflectionScale':[rScale],
                                          'materials':materials})
            sound = bs.newNode('sound',owner=self.node,attrs={'sound':factory.fuseSound,'volume':0.25})
            self.node.connectAttr('position',sound,'position')
            bsUtils.animate(self.node,'fuseLength',{0:1,fuseTime:0})

        # light the fuse!!!
        if self.bombType not in ('landMine','tnt','basketball'):
            bs.gameTimer(fuseTime,bs.WeakCall(self.handleMessage,ExplodeMessage()))

        bsUtils.animate(self.node,"modelScale",{0:0, 200:1.3, 260:1})

    def getSourcePlayer(self):
        """
        Returns a bs.Player representing the source of this bomb.
        """
        if self.sourcePlayer is None: return bs.Player(None) # empty player ref
        return self.sourcePlayer
        
    @classmethod
    def getFactory(cls):
        """
        Returns a shared bs.BombFactory object, creating it if necessary.
        """
        activity = bs.getActivity()
        try: return activity._sharedBombFactory
        except Exception:
            f = activity._sharedBombFactory = BombFactory()
            return f

    def onFinalize(self):
        bs.Actor.onFinalize(self)
        # release callbacks/refs so we don't wind up with dependency loops..
        self._explodeCallbacks = []
        
    def _handleDie(self,m):
        self.node.delete()
        
    def _handleOOB(self,m):
        self.handleMessage(bs.DieMessage())

    def _handleImpact(self,m):
        node,body = bs.getCollisionInfo("opposingNode","opposingBody")
        # if we're an impact bomb and we came from this node, don't explode...
        # alternately if we're hitting another impact-bomb from the same source, don't explode...
        try: nodeDelegate = node.getDelegate()
        except Exception: nodeDelegate = None
        if node.exists():
            if (self.bombType == 'impact' and
                (node is self.owner or (isinstance(nodeDelegate,Bomb) and nodeDelegate.bombType == 'impact' and nodeDelegate.owner is self.owner))): return
            elif (self.bombType == 'healing' and
                (node is self.owner or (isinstance(nodeDelegate,Bomb) and nodeDelegate.bombType == 'healing' and nodeDelegate.owner is self.owner))): return
            else: self.handleMessage(ExplodeMessage())

    def _handleDropped(self,m):
        if self.bombType == 'landMine':
            self.armTimer = bs.Timer(1250,bs.WeakCall(self.handleMessage,ArmMessage()))

        # once we've thrown a sticky bomb we can stick to it..
        elif self.bombType == 'sticky':
            def _safeSetAttr(node,attr,value):
                if node.exists(): setattr(node,attr,value)
            #bs.gameTimer(250,bs.Call(_safeSetAttr,self.node,'stickToOwner',True))
            bs.gameTimer(250,lambda: _safeSetAttr(self.node,'stickToOwner',True))

    def _handleSplat(self,m):
        node = bs.getCollisionInfo("opposingNode")
        if node is not self.owner and bs.getGameTime() - self._lastStickySoundTime > 1000:
            self._lastStickySoundTime = bs.getGameTime()
            bs.playSound(self.getFactory().stickyImpactSound,2.0,position=self.node.position)
            if node.getNodeType() == 'spaz': bs.playSound(self.getFactory().stickyImpactPlayerSound,1.0,position=self.node.position)

    def addExplodeCallback(self,call):
        """
        Add a call to be run when the bomb has exploded.
        The bomb and the new blast object are passed as arguments.
        """
        self._explodeCallbacks.append(call)
        
    def explode(self):
        """
        Blows up the bomb if it has not yet done so.
        """
        if self.bombType != 'basketball': # Basketball cannot be destroyed by bombs
            if self._exploded: return
            self._exploded = True
            activity = self.getActivity()
            if self.bombType == 'healing':
                bs.playSound(self.getFactory().healingSound,6,position=self.node.position)
            if activity is not None and self.node.exists():
                if self.bombType == 'dynamite':
                    blast = Blast(position=self.node.position,velocity=self.node.velocity,
                            blastRadius=self.blastRadius,blastType=self.bombType,sourcePlayer=self.sourcePlayer,hitType=self.hitType,hitSubType=self.hitSubType).autoRetain()
                    for c in self._explodeCallbacks: c(self,blast)
                    t = self.node.position
                    self.a = bs.Bomb(position=(t[0]+1, t[1], t[2]),velocity=(0,2,0),bombType='miniDynamite',sourcePlayer=self.sourcePlayer)
                    self.b = bs.Bomb(position=(t[0]-1, t[1], t[2]),velocity=(0,2,0),bombType='miniDynamite',sourcePlayer=self.sourcePlayer)
                    self.c = bs.Bomb(position=(t[0], t[1], t[2]+1),velocity=(0,2,0),bombType='miniDynamite',sourcePlayer=self.sourcePlayer)
                    self.d = bs.Bomb(position=(t[0], t[1], t[2]-1),velocity=(0,2,0),bombType='miniDynamite',sourcePlayer=self.sourcePlayer)
                    self.a2 = bs.Bomb(position=(t[0]+2, t[1], t[2]),velocity=(0,2,0),bombType='miniDynamite',sourcePlayer=self.sourcePlayer)
                    self.b2 = bs.Bomb(position=(t[0]-2, t[1], t[2]),velocity=(0,2,0),bombType='miniDynamite',sourcePlayer=self.sourcePlayer)
                    self.c2 = bs.Bomb(position=(t[0], t[1], t[2]+2),velocity=(0,2,0),bombType='miniDynamite',sourcePlayer=self.sourcePlayer)
                    self.d2 = bs.Bomb(position=(t[0], t[1], t[2]-2),velocity=(0,2,0),bombType='miniDynamite',sourcePlayer=self.sourcePlayer)
                    self.a3 = bs.Bomb(position=(t[0]+3, t[1], t[2]),velocity=(0,2,0),bombType='miniDynamite',sourcePlayer=self.sourcePlayer)
                    self.b3 = bs.Bomb(position=(t[0]-3, t[1], t[2]),velocity=(0,2,0),bombType='miniDynamite',sourcePlayer=self.sourcePlayer)
                    self.c3 = bs.Bomb(position=(t[0], t[1], t[2]+3),velocity=(0,2,0),bombType='miniDynamite',sourcePlayer=self.sourcePlayer)
                    self.d3 = bs.Bomb(position=(t[0], t[1], t[2]-3),velocity=(0,2,0),bombType='miniDynamite',sourcePlayer=self.sourcePlayer)
                    self.a4 = bs.Bomb(position=(t[0]+4, t[1], t[2]),velocity=(0,2,0),bombType='miniDynamite',sourcePlayer=self.sourcePlayer)
                    self.b4 = bs.Bomb(position=(t[0]-4, t[1], t[2]),velocity=(0,2,0),bombType='miniDynamite',sourcePlayer=self.sourcePlayer)
                    self.c4 = bs.Bomb(position=(t[0], t[1], t[2]+4),velocity=(0,2,0),bombType='miniDynamite',sourcePlayer=self.sourcePlayer)
                    self.d4 = bs.Bomb(position=(t[0], t[1], t[2]-4),velocity=(0,2,0),bombType='miniDynamite',sourcePlayer=self.sourcePlayer)
                elif self.bombType == 'fire': # Fire bomb creates a fire splat
                    factory = self.getFactory()
                    blast = Blast(position=self.node.position,velocity=self.node.velocity,
                            blastRadius=self.blastRadius,blastType=self.bombType,sourcePlayer=self.sourcePlayer,hitType=self.hitType,hitSubType=self.hitSubType).autoRetain()
                    for c in self._explodeCallbacks: c(self,blast)
                    print 'Working!'
                    self.fireLight = bs.newNode('light',
                            attrs={'position':self.node.position,
                                    'color': (0.5,0.5,0),
                                    'volumeIntensityScale': 1.0}) 
                    bs.animate(self.fireLight,'intensity',{0:0,250:2.0,5000:1.8, 5250:0.5, 8000:0},loop=False)
                    self.fireAttack = bs.newNode('region',
                                attrs={'position':(self.node.position[0],self.node.position[1]-0.1,self.node.position[2]), # move down and squished a bit so the fire affects the floor
                                        'scale':(self.blastRadius,self.blastRadius,self.blastRadius*0.25),
                                        'type':'sphere',
                                        'materials':(factory.blastMaterial,bs.getSharedObject('attackMaterial'))},
                                delegate=self)
                    bs.gameTimer(5000,self.fireAttack.delete)
                elif self.bombType == 'hijump':
                    blast = Blast(position=(self.node.position[0],self.node.position[1]-0.95,self.node.position[2]),velocity=self.node.velocity,
                            blastRadius=self.blastRadius,blastType=self.bombType,sourcePlayer=self.sourcePlayer,hitType=self.hitType,hitSubType=self.hitSubType).autoRetain()
                    for c in self._explodeCallbacks: c(self,blast)
                else:
                    blast = Blast(position=self.node.position,velocity=self.node.velocity,
                                blastRadius=self.blastRadius,blastType=self.bombType,sourcePlayer=self.sourcePlayer,hitType=self.hitType,hitSubType=self.hitSubType).autoRetain()
                    for c in self._explodeCallbacks: c(self,blast)
            # we blew up so we need to go away
            bs.gameTimer(1,bs.WeakCall(self.handleMessage,bs.DieMessage()))
        

    def _handleWarn(self,m):
        if self.textureSequence.exists():
            self.textureSequence.rate = 30
            bs.playSound(self.getFactory().warnSound,0.5,position=self.node.position)

    def _addMaterial(self,material):
        if not self.node.exists(): return
        materials = self.node.materials
        if not material in materials:
            self.node.materials = materials + (material,)
            
    def deploy(self):
        # Used for complex bomb animations, sounds or effects. Everything here is great!
        if not self.node.exists(): return
        factory = self.getFactory()
        if self.bombType == 'combat':
            self.light = bs.newNode('light',
                            attrs={'position':self.node.position,
                                    'color': (0.02,0.069,0.09),
                                    'volumeIntensityScale': 0.5})
            self.textureSequence = bs.newNode('textureSequence',
                                                owner=self.node,
                                                attrs={'inputTextures':(factory.combatTex,
                                                                        factory.combatLitTex),'rate':5})
            self.node.connectAttr('position',self.light,'position')
            self.textureSequence.connectAttr('outputTexture',self.node,'colorTexture')
            bs.animate(self.light,'intensity',{0:10, 200:0},loop=False)  
            
            bs.gameTimer(200,self.textureSequence.delete)
            bs.gameTimer(200,self.light.delete)
            bs.playSound(factory.combatBombDeployedSound,0.1,position=self.node.position)
        if self.bombType == 'grenade':
            t = self.node.position
            bs.playSound(factory.pinOutSound,1,position=self.node.position)
            bs.emitBGDynamics(position=(t[0], t[1], t[2]),velocity=(0.25, 0.25, 0.35),count=1,scale=1.5,spread=0.1,chunkType='rock');
            self.textureSequence = bs.newNode('textureSequence',
                                                owner=self.node,
                                                attrs={'inputTextures':(factory.grenade3Tex,
                                                                        factory.grenade2Tex,
                                                                        factory.grenade1Tex,
                                                                        factory.grenadeExTex),'rate':975})
            self.textureSequence.connectAttr('outputTexture',self.node,'colorTexture')       
            bsUtils.animate(self.node, 'modelScale', {0:0, 
                                   200:1.3,
                                   260:1,
                                   380:1.2,
                                   2950:1.0,
                                   3050:10.0,
                                   3100:12.0})
            bs.gameTimer(3250,self.textureSequence.delete)
        if self.bombType == 'dynamite':
            t = self.node.position
            bs.playSound(factory.dynamiteFuseSound,1.25,position=self.node.position)
        if self.bombType == 'ranger':
            bsUtils.animate(self.node, 'modelScale', {0:0,
                                   200:1.3,
                                   260:1,
                                   1000:1.10,
                                   1500:0.95,
                                   2000:1.05,
                                   2500:0.90,
                                   3000:1.1,
                                   3500:0.85,
                                   3800:1.15,
                                   3900:0.5,
                                   4000:5.0})
        if self.bombType == 'healing':
            bsUtils.animate(self.node, 'modelScale', {0:0,
                                   200:1.3,
                                   260:1,
                                   500:1.1,
                                   1000:1.0,
                                   1500:1.1,
                                   1950:1.0,
                                   2375:1.1,
                                   2725:1.0,
                                   3075:1.1,
                                   3350:1.0,
                                   3625:1.1,
                                   3725:1.0,
                                   3825:1.1,
                                   3925:1.0,
                                   4025:1.1,
                                   4125:1.0,
                                   4225:1.1,
                                   4325:1.0,
                                   4425:1.1,
                                   4525:1.0,
                                   4625:1.1,
                                   4725:1.0,
                                   4825:1.1,
                                   4925:1.0,
                                   5000:2.0})
        if self.bombType == 'hijump':
            self.light = bs.newNode('light',
                            attrs={'position':self.node.position,
                                    'color': (1,0.01,0.95),
                                    'volumeIntensityScale': 0.5})   
            bs.animate(self.light,'intensity',{0:2, 1000:0},loop=False)                                    
            bs.gameTimer(500,self.light.delete)
            
    def ready(self):
        # An alternative node for advanced sounds, effects or functions of bombs!
        if not self.node.exists(): return
        factory = self.getFactory()
        if self.bombType == 'combat':
            self.light = bs.newNode('light',
                            attrs={'position':self.node.position,
                                    'color': (0.0,0.49,0.7),
                                    'volumeIntensityScale': 0.5})
            self.textureSequence = bs.newNode('textureSequence',
                                                owner=self.node,
                                                attrs={'inputTextures':(factory.combatTex,
                                                                        factory.combatLitTex),'rate':10})
            self.node.connectAttr('position',self.light,'position')
            self.textureSequence.connectAttr('outputTexture',self.node,'colorTexture')
            
            bs.animate(self.light,'intensity',{0:2.5, 250:0},loop=False)  
            bs.gameTimer(250,self.textureSequence.delete)
            bs.gameTimer(250,self.light.delete)
            bs.playSound(factory.combatBombReadySound,0.1,position=self.node.position)
            
    def dropClusters(m,self):
        print 'Dropping Clusters!'
            
    def moreFlames(self):
        """
        Just a slightly delayed additional particle effects
        """
        bs.emitBGDynamics(self.node.position,emitType='distortion',spread=1.0)
        self.light = bs.newNode('light',
                            attrs={'position':self.node.position,
                                    'color': (1.0,0.49,0.15),
                                    'volumeIntensityScale': 0.5})
        bs.gameTimer(200,self.light.delete)  
        
    def arm(self):
        """
        Arms land-mines and impact-bombs so
        that they will explode on impact.
        """
        if not self.node.exists(): return
        factory = self.getFactory()
        if self.bombType == 'landMine':
            self.textureSequence = bs.newNode('textureSequence',
                                              owner=self.node,
                                              attrs={'inputTextures':(factory.landMineLitTex,
                                                                      factory.landMineTex),'rate':30})
            bs.gameTimer(500,self.textureSequence.delete)
            # we now make it explodable.
            bs.gameTimer(250,bs.WeakCall(self._addMaterial,factory.landMineBlastMaterial))
        elif self.bombType == 'impact':
            self.textureSequence = bs.newNode('textureSequence',
                                              owner=self.node,
                                              attrs={'inputTextures':(factory.impactLitTex,
                                                                      factory.impactTex,
                                                                      factory.impactTex),'rate':100})
            bs.gameTimer(250,bs.WeakCall(self._addMaterial,factory.landMineBlastMaterial))
        else:
            raise Exception('arm() should only be called on land-mines or impact bombs')
        self.textureSequence.connectAttr('outputTexture',self.node,'colorTexture')
        bs.playSound(factory.activateSound,0.5,position=self.node.position)
        
    def _handleHit(self,m):
        isPunch = (m.srcNode.exists() and m.srcNode.getNodeType() == 'spaz')

        # normal bombs are triggered by non-punch impacts..  impact-bombs by all impacts
        if not self._exploded and not isPunch or self.bombType in ['impact','landMine']:
            # also lets change the owner of the bomb to whoever is setting us off..
            # (this way points for big chain reactions go to the person causing them)
            if m.sourcePlayer not in [None]:
                self.sourcePlayer = m.sourcePlayer

                # also inherit the hit type (if a landmine sets off by a bomb, the credit should go to the mine)
                # the exception is TNT.  TNT always gets credit. The same thing goes to Dynamite Packs.
                if self.bombType != 'tnt' and self.bombType != 'dynamite':
                    self.hitType = m.hitType
                    self.hitSubType = m.hitSubType

            if m.hitSubType != 'healing' and m.hitSubType != 'hijump' and m.hitSubType != 'knocker': # Only the bombs not mentioned in this line will cause other bombs to explode
                bs.gameTimer(100+int(random.random()*100),bs.WeakCall(self.handleMessage,ExplodeMessage()))
        self.node.handleMessage("impulse",m.pos[0],m.pos[1],m.pos[2],
                                m.velocity[0],m.velocity[1],m.velocity[2],
                                m.magnitude,m.velocityMagnitude,m.radius,0,m.velocity[0],m.velocity[1],m.velocity[2])

        if m.srcNode.exists():
            pass
            #print 'FIXME HANDLE KICKBACK ON BOMB IMPACT'
            # bs.nodeMessage(m.srcNode,"impulse",m.srcBody,m.pos[0],m.pos[1],m.pos[2],
            #                     -0.5*m.force[0],-0.75*m.force[1],-0.5*m.force[2])
            
    def dissolve(self):
        """
        This command basically makes the bomb die, because of the Healing Bomb.
        """
        bs.playSound(self.getFactory().hissSound,3,position=self.node.position)
        if self.bombType != 'basketball': self.handleMessage(bs.DieMessage())
        
    def handleMessage(self,m):
        if isinstance(m,ExplodeMessage): self.explode()
        elif isinstance(m,ImpactMessage): self._handleImpact(m)
        elif isinstance(m,bs.PickedUpMessage):
            # change our source to whoever just picked us up *only* if its None
            # this way we can get points for killing bots with their own bombs
            # hmm would there be a downside to this?...
            if self.sourcePlayer is not None:
                self.sourcePlayer = m.node.sourcePlayer
        elif isinstance(m,SplatMessage): self._handleSplat(m)
        elif isinstance(m,bs.DroppedMessage): self._handleDropped(m)
        elif isinstance(m,bs.HitMessage): self._handleHit(m)
        elif isinstance(m,bs.DieMessage): self._handleDie(m)
        elif isinstance(m,bs.OutOfBoundsMessage): self._handleOOB(m)
        elif isinstance(m,ArmMessage): self.arm()
        elif isinstance(m,WarnMessage): self._handleWarn(m)
        elif isinstance(m,bs.HealMessage): self.dissolve()
        elif isinstance(m,ReadyMessage): self.ready()
        elif isinstance(m,DeployMessage): self.deploy()
        else: bs.Actor.handleMessage(self,m)

class TNTSpawner(object):
    """
    category: Game Flow Classes

    Regenerates TNT at a given point in space every now and then.
    """
    def __init__(self,position,respawnTime=30000):
        """
        Instantiate with a given position and respawnTime (in milliseconds).
        """
        self._position = position
        self._tnt = None
        self._update()
        self._updateTimer = bs.Timer(1000,bs.WeakCall(self._update),repeat=True)
        self._respawnTime = int(random.uniform(0.8,1.2)*respawnTime)
        self._waitTime = 0
        
    def _update(self):
        tntAlive = self._tnt is not None and self._tnt.node.exists()
        if not tntAlive:
            # respawn if its been long enough.. otherwise just increment our how-long-since-we-died value
            if self._tnt is None or self._waitTime >= self._respawnTime:
                self._tnt = Bomb(position=self._position,bombType='tnt')
                self._waitTime = 0
            else: self._waitTime += 1000
