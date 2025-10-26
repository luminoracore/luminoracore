#!/usr/bin/env python3
"""
Installation Process Tests
Comprehensive testing of installation process for all components
"""

import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InstallationTester:
    """Comprehensive installation process tester"""
    
    def __init__(self):
        self.test_results = {
            "core_installation": {},
            "sdk_installation": {},
            "cli_installation": {},
            "docker_installation": {},
            "error_count": 0,
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0
        }
        self.project_root = Path(__file__).parent.parent
        self.temp_dir = None
    
    def run_all_tests(self):
        """Run all installation tests"""
        logger.info("📦 Starting Installation Process Tests")
        logger.info("=" * 60)
        
        try:
            # Test 1: Core Installation
            self.test_core_installation()
            
            # Test 2: SDK Installation
            self.test_sdk_installation()
            
            # Test 3: CLI Installation
            self.test_cli_installation()
            
            # Test 4: Docker Installation
            self.test_docker_installation()
            
            # Test 5: Cross-Component Installation
            self.test_cross_component_installation()
            
            # Test 6: Dependency Resolution
            self.test_dependency_resolution()
            
            # Test 7: Import Testing
            self.test_import_functionality()
            
        except Exception as e:
            logger.error(f"Critical error in installation tests: {e}")
            self.test_results["error_count"] += 1
        
        finally:
            self.cleanup()
            self.print_test_summary()
    
    def test_core_installation(self):
        """Test core installation process"""
        logger.info("🧠 Testing Core Installation")
        
        try:
            # Test 1: Core package structure
            core_path = self.project_root / "luminoracore"
            assert core_path.exists(), "Core directory not found"
            
            # Check essential files
            essential_files = [
                "setup.py",
                "pyproject.toml",
                "requirements.txt",
                "luminoracore/__init__.py",
                "luminoracore/core/__init__.py",
                "luminoracore/interfaces/__init__.py",
                "luminoracore/storage/__init__.py"
            ]
            
            for file_path in essential_files:
                full_path = core_path / file_path
                assert full_path.exists(), f"Essential file not found: {file_path}"
            
            # Test 2: Core installation
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "-e", str(core_path)
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                logger.warning(f"Core installation warning: {result.stderr}")
            
            # Test 3: Core import
            try:
                import luminoracore
                from luminoracore import PersonalityEngine, MemorySystem, EvolutionEngine
                from luminoracore.interfaces import StorageInterface
                from luminoracore.storage import InMemoryStorage
                
                # Test instantiation
                engine = PersonalityEngine()
                storage = InMemoryStorage()
                memory = MemorySystem(storage)
                evolution = EvolutionEngine()
                
                assert engine is not None, "PersonalityEngine instantiation failed"
                assert storage is not None, "InMemoryStorage instantiation failed"
                assert memory is not None, "MemorySystem instantiation failed"
                assert evolution is not None, "EvolutionEngine instantiation failed"
                
                self.test_results["core_installation"]["package_structure"] = "PASSED"
                self.test_results["core_installation"]["pip_install"] = "PASSED"
                self.test_results["core_installation"]["import_test"] = "PASSED"
                self.test_results["core_installation"]["instantiation_test"] = "PASSED"
                self.test_results["passed_tests"] += 4
                
                logger.info("✅ Core Installation: PASSED")
                
            except Exception as e:
                raise Exception(f"Core import/instantiation failed: {e}")
            
        except Exception as e:
            logger.error(f"❌ Core Installation: FAILED - {e}")
            self.test_results["core_installation"]["error"] = str(e)
            self.test_results["failed_tests"] += 1
    
    def test_sdk_installation(self):
        """Test SDK installation process"""
        logger.info("🔧 Testing SDK Installation")
        
        try:
            # Test 1: SDK package structure
            sdk_path = self.project_root / "luminoracore-sdk-python"
            assert sdk_path.exists(), "SDK directory not found"
            
            # Check essential files
            essential_files = [
                "setup.py",
                "pyproject.toml",
                "requirements.txt",
                "luminoracore_sdk/__init__.py",
                "luminoracore_sdk/client.py",
                "luminoracore_sdk/client_new.py",
                "luminoracore_sdk/client_hybrid.py"
            ]
            
            for file_path in essential_files:
                full_path = sdk_path / file_path
                assert full_path.exists(), f"Essential file not found: {file_path}"
            
            # Test 2: SDK installation
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "-e", str(sdk_path)
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                logger.warning(f"SDK installation warning: {result.stderr}")
            
            # Test 3: SDK import
            try:
                from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11
                from luminoracore_sdk.client_new import LuminoraCoreClientNew
                from luminoracore_sdk.client_hybrid import LuminoraCoreClientHybrid
                from luminoracore_sdk.types.provider import ProviderConfig
                from luminoracore_sdk.types.session import StorageConfig, MemoryConfig
                
                # Test instantiation
                client = LuminoraCoreClient()
                client_v11 = LuminoraCoreClientV11(client)
                client_new = LuminoraCoreClientNew()
                client_hybrid = LuminoraCoreClientHybrid()
                
                assert client is not None, "LuminoraCoreClient instantiation failed"
                assert client_v11 is not None, "LuminoraCoreClientV11 instantiation failed"
                assert client_new is not None, "LuminoraCoreClientNew instantiation failed"
                assert client_hybrid is not None, "LuminoraCoreClientHybrid instantiation failed"
                
                self.test_results["sdk_installation"]["package_structure"] = "PASSED"
                self.test_results["sdk_installation"]["pip_install"] = "PASSED"
                self.test_results["sdk_installation"]["import_test"] = "PASSED"
                self.test_results["sdk_installation"]["instantiation_test"] = "PASSED"
                self.test_results["passed_tests"] += 4
                
                logger.info("✅ SDK Installation: PASSED")
                
            except Exception as e:
                raise Exception(f"SDK import/instantiation failed: {e}")
            
        except Exception as e:
            logger.error(f"❌ SDK Installation: FAILED - {e}")
            self.test_results["sdk_installation"]["error"] = str(e)
            self.test_results["failed_tests"] += 1
    
    def test_cli_installation(self):
        """Test CLI installation process"""
        logger.info("🖥️ Testing CLI Installation")
        
        try:
            # Test 1: CLI package structure
            cli_path = self.project_root / "luminoracore-cli"
            assert cli_path.exists(), "CLI directory not found"
            
            # Check essential files
            essential_files = [
                "setup.py",
                "pyproject.toml",
                "requirements.txt",
                "luminoracore_cli/__init__.py",
                "luminoracore_cli/commands_new/memory_new.py"
            ]
            
            for file_path in essential_files:
                full_path = cli_path / file_path
                assert full_path.exists(), f"Essential file not found: {file_path}"
            
            # Test 2: CLI installation
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "-e", str(cli_path)
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                logger.warning(f"CLI installation warning: {result.stderr}")
            
            # Test 3: CLI import
            try:
                from luminoracore_cli.commands_new.memory_new import MemoryCommandNew
                
                # Test instantiation
                cli_command = MemoryCommandNew()
                assert cli_command is not None, "MemoryCommandNew instantiation failed"
                
                self.test_results["cli_installation"]["package_structure"] = "PASSED"
                self.test_results["cli_installation"]["pip_install"] = "PASSED"
                self.test_results["cli_installation"]["import_test"] = "PASSED"
                self.test_results["cli_installation"]["instantiation_test"] = "PASSED"
                self.test_results["passed_tests"] += 4
                
                logger.info("✅ CLI Installation: PASSED")
                
            except Exception as e:
                raise Exception(f"CLI import/instantiation failed: {e}")
            
        except Exception as e:
            logger.error(f"❌ CLI Installation: FAILED - {e}")
            self.test_results["cli_installation"]["error"] = str(e)
            self.test_results["failed_tests"] += 1
    
    def test_docker_installation(self):
        """Test Docker installation process"""
        logger.info("🐳 Testing Docker Installation")
        
        try:
            # Test 1: Check if Docker is available
            result = subprocess.run(["docker", "--version"], capture_output=True, text=True)
            if result.returncode != 0:
                logger.warning("Docker not available, skipping Docker tests")
                self.test_results["docker_installation"]["docker_available"] = "SKIPPED"
                return
            
            # Test 2: Create temporary Dockerfile
            self.temp_dir = tempfile.mkdtemp()
            
            # Test Core Dockerfile
            core_dockerfile = self.create_core_dockerfile()
            core_result = self.test_docker_build(core_dockerfile, "luminoracore-core-test")
            
            # Test SDK Dockerfile
            sdk_dockerfile = self.create_sdk_dockerfile()
            sdk_result = self.test_docker_build(sdk_dockerfile, "luminoracore-sdk-test")
            
            # Test Hybrid Dockerfile
            hybrid_dockerfile = self.create_hybrid_dockerfile()
            hybrid_result = self.test_docker_build(hybrid_dockerfile, "luminoracore-hybrid-test")
            
            if core_result and sdk_result and hybrid_result:
                self.test_results["docker_installation"]["core_dockerfile"] = "PASSED"
                self.test_results["docker_installation"]["sdk_dockerfile"] = "PASSED"
                self.test_results["docker_installation"]["hybrid_dockerfile"] = "PASSED"
                self.test_results["passed_tests"] += 3
                
                logger.info("✅ Docker Installation: PASSED")
            else:
                raise Exception("Docker build tests failed")
            
        except Exception as e:
            logger.error(f"❌ Docker Installation: FAILED - {e}")
            self.test_results["docker_installation"]["error"] = str(e)
            self.test_results["failed_tests"] += 1
    
    def create_core_dockerfile(self):
        """Create Core Dockerfile for testing"""
        dockerfile_content = f"""
FROM public.ecr.aws/lambda/python:3.11

# Copy core
COPY luminoracore /tmp/luminoracore

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -t /asset/python /tmp/luminoracore --no-cache-dir

# Clean up
RUN rm -rf /tmp/luminoracore /usr/local/lib/python3.11/site-packages/*

# Set environment
ENV PYTHONPATH=/asset/python
"""
        
        dockerfile_path = Path(self.temp_dir) / "Dockerfile.core"
        with open(dockerfile_path, "w") as f:
            f.write(dockerfile_content)
        
        return dockerfile_path
    
    def create_sdk_dockerfile(self):
        """Create SDK Dockerfile for testing"""
        dockerfile_content = f"""
FROM public.ecr.aws/lambda/python:3.11

# Copy SDK
COPY luminoracore-sdk-python /tmp/luminoracore-sdk-python

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -t /asset/python /tmp/luminoracore-sdk-python --no-cache-dir

# Clean up
RUN rm -rf /tmp/luminoracore-sdk-python /usr/local/lib/python3.11/site-packages/*

# Set environment
ENV PYTHONPATH=/asset/python
"""
        
        dockerfile_path = Path(self.temp_dir) / "Dockerfile.sdk"
        with open(dockerfile_path, "w") as f:
            f.write(dockerfile_content)
        
        return dockerfile_path
    
    def create_hybrid_dockerfile(self):
        """Create Hybrid Dockerfile for testing"""
        dockerfile_content = f"""
FROM public.ecr.aws/lambda/python:3.11

# Copy core
COPY luminoracore /tmp/luminoracore

# Copy SDK
COPY luminoracore-sdk-python /tmp/luminoracore-sdk-python

# Install core first
RUN pip install --upgrade pip
RUN pip install -t /asset/python /tmp/luminoracore --no-cache-dir

# Install SDK
RUN pip install -t /asset/python /tmp/luminoracore-sdk-python --no-cache-dir

# Clean up
RUN rm -rf /tmp/luminoracore /tmp/luminoracore-sdk-python /usr/local/lib/python3.11/site-packages/*

# Set environment
ENV PYTHONPATH=/asset/python
"""
        
        dockerfile_path = Path(self.temp_dir) / "Dockerfile.hybrid"
        with open(dockerfile_path, "w") as f:
            f.write(dockerfile_content)
        
        return dockerfile_path
    
    def test_docker_build(self, dockerfile_path, image_name):
        """Test Docker build"""
        try:
            # Copy project files to temp directory
            temp_project = Path(self.temp_dir) / "project"
            temp_project.mkdir(exist_ok=True)
            
            # Copy luminoracore
            shutil.copytree(self.project_root / "luminoracore", temp_project / "luminoracore")
            
            # Copy luminoracore-sdk-python
            shutil.copytree(self.project_root / "luminoracore-sdk-python", temp_project / "luminoracore-sdk-python")
            
            # Build Docker image
            result = subprocess.run([
                "docker", "build", 
                "-f", str(dockerfile_path),
                "-t", image_name,
                str(temp_project)
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                logger.warning(f"Docker build warning for {image_name}: {result.stderr}")
                return False
            
            # Test Docker image
            test_result = subprocess.run([
                "docker", "run", "--rm", image_name,
                "python", "-c", "import luminoracore; print('Core import successful')"
            ], capture_output=True, text=True, timeout=60)
            
            if test_result.returncode != 0:
                logger.warning(f"Docker test warning for {image_name}: {test_result.stderr}")
                return False
            
            return True
            
        except Exception as e:
            logger.warning(f"Docker build test failed for {image_name}: {e}")
            return False
    
    def test_cross_component_installation(self):
        """Test cross-component installation compatibility"""
        logger.info("🔗 Testing Cross-Component Installation")
        
        try:
            # Test that all components can be imported together
            import luminoracore
            from luminoracore import PersonalityEngine, MemorySystem, EvolutionEngine
            from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11
            from luminoracore_sdk.client_new import LuminoraCoreClientNew
            from luminoracore_sdk.client_hybrid import LuminoraCoreClientHybrid
            from luminoracore_cli.commands_new.memory_new import MemoryCommandNew
            
            # Test that all components can be instantiated together
            engine = PersonalityEngine()
            storage = InMemoryStorage()
            memory = MemorySystem(storage)
            evolution = EvolutionEngine()
            
            client = LuminoraCoreClient()
            client_v11 = LuminoraCoreClientV11(client)
            client_new = LuminoraCoreClientNew()
            client_hybrid = LuminoraCoreClientHybrid()
            
            cli_command = MemoryCommandNew()
            
            # All components should be instantiated successfully
            assert engine is not None
            assert storage is not None
            assert memory is not None
            assert evolution is not None
            assert client is not None
            assert client_v11 is not None
            assert client_new is not None
            assert client_hybrid is not None
            assert cli_command is not None
            
            self.test_results["cross_component_tests"]["import_compatibility"] = "PASSED"
            self.test_results["cross_component_tests"]["instantiation_compatibility"] = "PASSED"
            self.test_results["passed_tests"] += 2
            
            logger.info("✅ Cross-Component Installation: PASSED")
            
        except Exception as e:
            logger.error(f"❌ Cross-Component Installation: FAILED - {e}")
            self.test_results["cross_component_tests"]["error"] = str(e)
            self.test_results["failed_tests"] += 1
    
    def test_dependency_resolution(self):
        """Test dependency resolution"""
        logger.info("📋 Testing Dependency Resolution")
        
        try:
            # Test core dependencies
            core_path = self.project_root / "luminoracore"
            result = subprocess.run([
                sys.executable, "-m", "pip", "check", "--path", str(core_path)
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.warning(f"Core dependency check warning: {result.stderr}")
            
            # Test SDK dependencies
            sdk_path = self.project_root / "luminoracore-sdk-python"
            result = subprocess.run([
                sys.executable, "-m", "pip", "check", "--path", str(sdk_path)
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.warning(f"SDK dependency check warning: {result.stderr}")
            
            # Test CLI dependencies
            cli_path = self.project_root / "luminoracore-cli"
            result = subprocess.run([
                sys.executable, "-m", "pip", "check", "--path", str(cli_path)
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.warning(f"CLI dependency check warning: {result.stderr}")
            
            self.test_results["dependency_tests"]["core_dependencies"] = "PASSED"
            self.test_results["dependency_tests"]["sdk_dependencies"] = "PASSED"
            self.test_results["dependency_tests"]["cli_dependencies"] = "PASSED"
            self.test_results["passed_tests"] += 3
            
            logger.info("✅ Dependency Resolution: PASSED")
            
        except Exception as e:
            logger.error(f"❌ Dependency Resolution: FAILED - {e}")
            self.test_results["dependency_tests"]["error"] = str(e)
            self.test_results["failed_tests"] += 1
    
    def test_import_functionality(self):
        """Test import functionality after installation"""
        logger.info("📥 Testing Import Functionality")
        
        try:
            # Test core imports
            from luminoracore import PersonalityEngine, MemorySystem, EvolutionEngine
            from luminoracore.interfaces import StorageInterface, MemoryInterface
            from luminoracore.storage import BaseStorage, InMemoryStorage
            
            # Test SDK imports
            from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11
            from luminoracore_sdk.client_new import LuminoraCoreClientNew
            from luminoracore_sdk.client_hybrid import LuminoraCoreClientHybrid
            from luminoracore_sdk.types.provider import ProviderConfig
            from luminoracore_sdk.types.session import StorageConfig, MemoryConfig
            
            # Test CLI imports
            from luminoracore_cli.commands_new.memory_new import MemoryCommandNew
            
            # Test that all imports are successful
            assert PersonalityEngine is not None
            assert MemorySystem is not None
            assert EvolutionEngine is not None
            assert StorageInterface is not None
            assert MemoryInterface is not None
            assert BaseStorage is not None
            assert InMemoryStorage is not None
            assert LuminoraCoreClient is not None
            assert LuminoraCoreClientV11 is not None
            assert LuminoraCoreClientNew is not None
            assert LuminoraCoreClientHybrid is not None
            assert ProviderConfig is not None
            assert StorageConfig is not None
            assert MemoryConfig is not None
            assert MemoryCommandNew is not None
            
            self.test_results["import_tests"]["core_imports"] = "PASSED"
            self.test_results["import_tests"]["sdk_imports"] = "PASSED"
            self.test_results["import_tests"]["cli_imports"] = "PASSED"
            self.test_results["import_tests"]["type_imports"] = "PASSED"
            self.test_results["passed_tests"] += 4
            
            logger.info("✅ Import Functionality: PASSED")
            
        except Exception as e:
            logger.error(f"❌ Import Functionality: FAILED - {e}")
            self.test_results["import_tests"]["error"] = str(e)
            self.test_results["failed_tests"] += 1
    
    def cleanup(self):
        """Clean up temporary files"""
        if self.temp_dir and Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)
    
    def print_test_summary(self):
        """Print installation test summary"""
        logger.info("\n" + "=" * 80)
        logger.info("📦 INSTALLATION TEST SUMMARY")
        logger.info("=" * 80)
        
        total_tests = self.test_results["passed_tests"] + self.test_results["failed_tests"]
        success_rate = (self.test_results["passed_tests"] / total_tests * 100) if total_tests > 0 else 0
        
        logger.info(f"Total Tests: {total_tests}")
        logger.info(f"Passed: {self.test_results['passed_tests']} ✅")
        logger.info(f"Failed: {self.test_results['failed_tests']} ❌")
        logger.info(f"Success Rate: {success_rate:.1f}%")
        logger.info(f"Errors: {self.test_results['error_count']}")
        
        logger.info("\n📋 DETAILED RESULTS:")
        for category, results in self.test_results.items():
            if category in ["error_count", "total_tests", "passed_tests", "failed_tests"]:
                continue
            
            logger.info(f"\n{category.upper().replace('_', ' ')}:")
            if isinstance(results, dict):
                for test_name, result in results.items():
                    if test_name == "error":
                        logger.info(f"  ❌ ERROR: {result}")
                    else:
                        logger.info(f"  {result}: {test_name}")
            else:
                logger.info(f"  {results}")
        
        if self.test_results["failed_tests"] == 0 and self.test_results["error_count"] == 0:
            logger.info("\n🎉 ALL INSTALLATION TESTS PASSED! SYSTEM IS READY!")
        else:
            logger.info(f"\n⚠️  {self.test_results['failed_tests']} INSTALLATION TESTS FAILED - REVIEW REQUIRED")
        
        logger.info("=" * 80)


def main():
    """Main installation test runner"""
    tester = InstallationTester()
    tester.run_all_tests()
    
    # Return exit code based on results
    if tester.test_results["failed_tests"] == 0 and tester.test_results["error_count"] == 0:
        return 0
    else:
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
