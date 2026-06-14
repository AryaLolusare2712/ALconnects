import { useEffect, useRef } from "react";
import * as THREE from "three";

export default function NeuralScene() {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const scene = new THREE.Scene();
    const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    const camera = new THREE.PerspectiveCamera(46, 1, 0.1, 100);
    camera.position.set(0, 0.35, 7.2);

    const group = new THREE.Group();
    scene.add(group);

    const core = new THREE.Mesh(
      new THREE.IcosahedronGeometry(1.45, 3),
      new THREE.MeshStandardMaterial({
        color: 0x60f3da,
        emissive: 0x11564f,
        roughness: 0.38,
        metalness: 0.48,
        wireframe: true,
      }),
    );
    group.add(core);

    const nodeMaterial = new THREE.MeshStandardMaterial({
      color: 0xf2c46f,
      emissive: 0x4d3210,
      roughness: 0.28,
      metalness: 0.38,
    });
    const lineMaterial = new THREE.LineBasicMaterial({ color: 0x73e0cf, transparent: true, opacity: 0.34 });
    const smallNode = new THREE.SphereGeometry(0.055, 16, 16);
    const lineGeometries = [];
    const points = [];

    for (let ring = 0; ring < 3; ring += 1) {
      const count = ring === 1 ? 18 : 14;
      const radius = 2.15 + ring * 0.55;
      const tilt = ring * 0.72;

      for (let index = 0; index < count; index += 1) {
        const angle = (index / count) * Math.PI * 2;
        const point = new THREE.Vector3(
          Math.cos(angle) * radius,
          Math.sin(angle + tilt) * 0.55,
          Math.sin(angle) * radius,
        );

        points.push(point);
        const node = new THREE.Mesh(smallNode, nodeMaterial);
        node.position.copy(point);
        group.add(node);
      }
    }

    for (let i = 0; i < points.length; i += 3) {
      const geometry = new THREE.BufferGeometry().setFromPoints([points[i], points[(i + 9) % points.length]]);
      lineGeometries.push(geometry);
      group.add(new THREE.Line(geometry, lineMaterial));
    }

    const particlesGeometry = new THREE.BufferGeometry();
    const particleCount = 700;
    const positions = new Float32Array(particleCount * 3);
    for (let i = 0; i < particleCount; i += 1) {
      positions[i * 3] = (Math.random() - 0.5) * 10;
      positions[i * 3 + 1] = (Math.random() - 0.5) * 8;
      positions[i * 3 + 2] = (Math.random() - 0.5) * 8;
    }
    particlesGeometry.setAttribute("position", new THREE.BufferAttribute(positions, 3));
    const particles = new THREE.Points(
      particlesGeometry,
      new THREE.PointsMaterial({ color: 0xffffff, size: 0.012, transparent: true, opacity: 0.5 }),
    );
    scene.add(particles);

    scene.add(new THREE.AmbientLight(0xffffff, 0.55));
    const keyLight = new THREE.PointLight(0x60f3da, 24, 12);
    keyLight.position.set(3, 3, 4);
    scene.add(keyLight);
    const warmLight = new THREE.PointLight(0xf2c46f, 12, 11);
    warmLight.position.set(-3, -2, 3);
    scene.add(warmLight);

    const resize = () => {
      const { width, height } = canvas.getBoundingClientRect();
      renderer.setSize(width, height, false);
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
    };

    let frameId;
    const clock = new THREE.Clock();
    const animate = () => {
      const elapsed = clock.getElapsedTime();
      group.rotation.y = elapsed * 0.22;
      group.rotation.x = Math.sin(elapsed * 0.38) * 0.14;
      core.rotation.z = elapsed * 0.34;
      particles.rotation.y = elapsed * 0.035;
      renderer.render(scene, camera);
      frameId = requestAnimationFrame(animate);
    };

    resize();
    animate();
    window.addEventListener("resize", resize);

    return () => {
      cancelAnimationFrame(frameId);
      window.removeEventListener("resize", resize);
      renderer.dispose();
      particlesGeometry.dispose();
      smallNode.dispose();
      core.geometry.dispose();
      core.material.dispose();
      particles.material.dispose();
      nodeMaterial.dispose();
      lineMaterial.dispose();
      lineGeometries.forEach((geometry) => geometry.dispose());
    };
  }, []);

  return (
    <div className="scene-wrap" aria-hidden="true">
      <canvas ref={canvasRef} />
      <div className="scene-caption">
        <strong>GenAI system map</strong>
        <span>retrieval · agents · APIs</span>
      </div>
    </div>
  );
}
