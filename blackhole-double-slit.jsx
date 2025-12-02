import React, { useState, useEffect, useRef } from 'react';
import { Play, Pause, RotateCcw } from 'lucide-react';

const BlackHoleDoubleSlit = () => {
  const canvasRef = useRef(null);
  const [isRunning, setIsRunning] = useState(false);
  const [showWormholes, setShowWormholes] = useState(true);
  const [showParticles, setShowParticles] = useState(true);
  const [detectMode, setDetectMode] = useState('none'); // 'none', 'direct', 'indirect'
  const [particles, setParticles] = useState([]);
  const [blackHoles, setBlackHoles] = useState([]);
  const [detectionScreen, setDetectionScreen] = useState([]);
  const animationRef = useRef(null);
  const timeRef = useRef(0);

  const width = 800;
  const height = 600;
  const slitY = 150;
  const screenX = 700;
  
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    // Initialize detection screen
    if (detectionScreen.length === 0) {
      const newScreen = Array(height).fill(0);
      setDetectionScreen(newScreen);
    }

    const draw = () => {
      // Clear canvas
      ctx.fillStyle = '#0a0a0a';
      ctx.fillRect(0, 0, width, height);

      // Draw double slit barrier
      ctx.fillStyle = '#444';
      ctx.fillRect(slitY - 5, 0, 10, height);
      
      // Draw slits
      const slitWidth = 40;
      const slitGap = 100;
      const centerY = height / 2;
      const slit1Y = centerY - slitGap / 2;
      const slit2Y = centerY + slitGap / 2;
      
      ctx.fillStyle = '#0a0a0a';
      ctx.fillRect(slitY - 5, slit1Y - slitWidth / 2, 10, slitWidth);
      ctx.fillRect(slitY - 5, slit2Y - slitWidth / 2, 10, slitWidth);

      // Draw detection screen
      ctx.fillStyle = '#222';
      ctx.fillRect(screenX - 2, 0, 4, height);

      // Draw interference pattern on screen
      for (let y = 0; y < height; y++) {
        const intensity = Math.min(255, detectionScreen[y] * 5);
        if (intensity > 0) {
          ctx.fillStyle = `rgba(100, 200, 255, ${intensity / 255})`;
          ctx.fillRect(screenX + 5, y, 20, 1);
        }
      }

      // Draw background particles
      if (showParticles) {
        particles.forEach(p => {
          const dist = Math.sqrt(Math.pow(p.x - p.bhX, 2) + Math.pow(p.y - p.bhY, 2));
          const influence = Math.max(0, 1 - dist / 80);
          
          ctx.fillStyle = `rgba(150, 150, 200, ${0.3 + influence * 0.5})`;
          ctx.beginPath();
          ctx.arc(p.x, p.y, 1 + influence * 2, 0, Math.PI * 2);
          ctx.fill();
        });
      }

      // Draw black holes and their effects
      blackHoles.forEach(bh => {
        // Draw gravitational field
        for (let r = 60; r > 0; r -= 15) {
          ctx.strokeStyle = `rgba(255, 100, 255, ${0.1 * (1 - r / 60)})`;
          ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.arc(bh.x, bh.y, r, 0, Math.PI * 2);
          ctx.stroke();
        }

        // Draw event horizon
        ctx.fillStyle = '#000';
        ctx.beginPath();
        ctx.arc(bh.x, bh.y, 8, 0, Math.PI * 2);
        ctx.fill();
        
        // Draw accretion disk effect
        ctx.strokeStyle = 'rgba(255, 150, 50, 0.6)';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(bh.x, bh.y, 12, 0, Math.PI * 2);
        ctx.stroke();

        // Draw wormhole connections if in superposition
        if (showWormholes && bh.inSuperposition && bh.x < slitY + 50) {
          // Connection to both slits
          const drawWormhole = (targetY) => {
            ctx.strokeStyle = 'rgba(100, 255, 200, 0.3)';
            ctx.lineWidth = 2;
            ctx.setLineDash([5, 5]);
            ctx.beginPath();
            ctx.moveTo(bh.x, bh.y);
            // Curved connection
            const midX = (bh.x + slitY) / 2;
            ctx.quadraticCurveTo(midX, targetY, slitY, targetY);
            ctx.stroke();
            ctx.setLineDash([]);

            // Draw wormhole mouth at slit
            ctx.fillStyle = 'rgba(100, 255, 200, 0.2)';
            ctx.beginPath();
            ctx.arc(slitY, targetY, 15, 0, Math.PI * 2);
            ctx.fill();
            ctx.strokeStyle = 'rgba(100, 255, 200, 0.5)';
            ctx.stroke();
          };

          drawWormhole(slit1Y);
          drawWormhole(slit2Y);
        }

        // Label
        if (bh.inSuperposition && detectMode === 'none') {
          ctx.fillStyle = '#fff';
          ctx.font = '12px monospace';
          ctx.fillText('Superposition', bh.x - 40, bh.y - 25);
        }
      });

      // Draw info text
      ctx.fillStyle = '#fff';
      ctx.font = '14px monospace';
      ctx.fillText(`Detection: ${detectMode}`, 10, 30);
      ctx.fillText(`Wormholes: ${showWormholes ? 'ON' : 'OFF'}`, 10, 50);
      ctx.fillText(`Particle Field: ${showParticles ? 'ON' : 'OFF'}`, 10, 70);
      
      if (detectMode === 'none') {
        ctx.fillText('Black hole in quantum superposition', 10, height - 40);
        ctx.fillText('(exists at both slits simultaneously)', 10, height - 20);
      } else if (detectMode === 'indirect') {
        ctx.fillText('Detecting via particle displacement', 10, height - 20);
      }
    };

    const animate = () => {
      if (!isRunning) return;

      timeRef.current += 0.016;

      // Spawn new black hole periodically
      if (Math.random() < 0.02 && blackHoles.length < 3) {
        setBlackHoles(prev => [...prev, {
          x: 20,
          y: height / 2 + (Math.random() - 0.5) * 40,
          vx: 2,
          vy: 0,
          inSuperposition: detectMode === 'none',
          pathY: null
        }]);
      }

      // Update black holes
      setBlackHoles(prev => prev.map(bh => {
        let newBh = { ...bh, x: bh.x + bh.vx };

        // Determine path when passing through slits
        if (bh.x < slitY && newBh.x >= slitY) {
          if (detectMode === 'none') {
            // In superposition - will interfere
            newBh.inSuperposition = true;
          } else {
            // Measured - collapse to one slit
            const slit1Y = height / 2 - 50;
            const slit2Y = height / 2 + 50;
            newBh.pathY = Math.random() < 0.5 ? slit1Y : slit2Y;
            newBh.y = newBh.pathY;
            newBh.inSuperposition = false;
          }
        }

        // After slits, if in superposition, create interference
        if (newBh.x > slitY + 50 && newBh.inSuperposition) {
          const distanceAfterSlit = newBh.x - slitY;
          const wavelength = 80;
          const slit1Y = height / 2 - 50;
          const slit2Y = height / 2 + 50;
          
          // Calculate interference pattern
          const phase = (distanceAfterSlit / wavelength) * Math.PI * 2;
          const amplitude = 30;
          newBh.y = height / 2 + amplitude * Math.sin(phase);
        }

        // Remove if off screen
        return newBh.x > width + 50 ? null : newBh;
      }).filter(Boolean));

      // Update background particles
      setParticles(prev => {
        // Add new particles
        let newParticles = [...prev];
        while (newParticles.length < 200) {
          newParticles.push({
            x: Math.random() * width,
            y: Math.random() * height,
            bhX: 0,
            bhY: 0
          });
        }

        // Update particle positions based on black hole gravity
        return newParticles.map(p => {
          let closestBh = { x: 0, y: 0, dist: Infinity };
          blackHoles.forEach(bh => {
            const dist = Math.sqrt(Math.pow(p.x - bh.x, 2) + Math.pow(p.y - bh.y, 2));
            if (dist < closestBh.dist) {
              closestBh = { x: bh.x, y: bh.y, dist };
            }
          });

          return {
            ...p,
            bhX: closestBh.x,
            bhY: closestBh.y
          };
        });
      });

      // Record hits on detection screen
      blackHoles.forEach(bh => {
        if (Math.abs(bh.x - screenX) < 5) {
          const y = Math.floor(bh.y);
          if (y >= 0 && y < height) {
            setDetectionScreen(prev => {
              const newScreen = [...prev];
              newScreen[y] = Math.min(50, newScreen[y] + 1);
              return newScreen;
            });
          }
        }
      });

      draw();
      animationRef.current = requestAnimationFrame(animate);
    };

    if (isRunning) {
      animate();
    } else {
      draw();
    }

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [isRunning, blackHoles, particles, detectionScreen, showWormholes, showParticles, detectMode]);

  const reset = () => {
    setBlackHoles([]);
    setParticles([]);
    setDetectionScreen(Array(height).fill(0));
    timeRef.current = 0;
  };

  return (
    <div className="w-full max-w-4xl mx-auto p-6 bg-gray-900 rounded-lg">
      <h1 className="text-2xl font-bold text-white mb-4">
        Black Hole Double-Slit Experiment
      </h1>
      
      <div className="mb-4 p-4 bg-gray-800 rounded text-sm text-gray-300">
        <p className="mb-2">
          <strong className="text-blue-300">Hypothesis:</strong> A quantum black hole creates wormholes when in superposition, 
          affecting particle displacement patterns differently than classical measurement.
        </p>
        <p>
          <strong className="text-purple-300">Detection modes:</strong> None (superposition) | Direct (which-path) | Indirect (particle wake)
        </p>
      </div>

      <canvas 
        ref={canvasRef} 
        width={width} 
        height={height}
        className="w-full border-2 border-gray-700 rounded mb-4"
      />

      <div className="grid grid-cols-2 gap-4 mb-4">
        <div className="space-y-2">
          <label className="text-white text-sm font-semibold block">Detection Mode:</label>
          <select 
            value={detectMode}
            onChange={(e) => {
              setDetectMode(e.target.value);
              reset();
            }}
            className="w-full p-2 bg-gray-800 text-white rounded border border-gray-600"
          >
            <option value="none">None (Quantum Superposition)</option>
            <option value="direct">Direct (Which-Path Detection)</option>
            <option value="indirect">Indirect (Particle Displacement)</option>
          </select>
        </div>

        <div className="space-y-2">
          <label className="text-white text-sm font-semibold block">Visualization:</label>
          <div className="space-y-1">
            <label className="flex items-center text-white text-sm">
              <input 
                type="checkbox" 
                checked={showWormholes}
                onChange={(e) => setShowWormholes(e.target.checked)}
                className="mr-2"
              />
              Show Wormhole Connections
            </label>
            <label className="flex items-center text-white text-sm">
              <input 
                type="checkbox" 
                checked={showParticles}
                onChange={(e) => setShowParticles(e.target.checked)}
                className="mr-2"
              />
              Show Particle Field
            </label>
          </div>
        </div>
      </div>

      <div className="flex gap-4">
        <button
          onClick={() => setIsRunning(!isRunning)}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded"
        >
          {isRunning ? <Pause size={20} /> : <Play size={20} />}
          {isRunning ? 'Pause' : 'Start'}
        </button>
        
        <button
          onClick={reset}
          className="flex items-center gap-2 px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded"
        >
          <RotateCcw size={20} />
          Reset
        </button>
      </div>

      <div className="mt-4 p-4 bg-gray-800 rounded text-sm text-gray-300 space-y-2">
        <p><strong className="text-green-300">Expected Results:</strong></p>
        <ul className="list-disc list-inside space-y-1 ml-2">
          <li><strong>No Detection:</strong> Interference pattern from wormhole-mediated superposition</li>
          <li><strong>Direct Detection:</strong> No interference (wave function collapse)</li>
          <li><strong>Indirect Detection:</strong> Novel pattern from particle displacement preserving some coherence?</li>
        </ul>
      </div>
    </div>
  );
};

export default BlackHoleDoubleSlit;
