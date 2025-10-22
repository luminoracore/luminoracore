#!/usr/bin/env python3
"""
LuminoraCore Framework - Automated Quality Validation Script

This script validates the entire framework to ensure there are no "cutre" (hacky)
implementations and that everything follows professional standards.

Author: LuminoraCore Team
Version: 1.0.0
"""

import os
import sys
import re
import json
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class Severity(Enum):
    """Issue severity levels."""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


@dataclass
class ValidationIssue:
    """Represents a validation issue found in the codebase."""
    severity: Severity
    category: str
    file_path: str
    line_number: Optional[int]
    description: str
    suggestion: str


class FrameworkValidator:
    """Validates the LuminoraCore framework for professional standards."""
    
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path)
        self.issues: List[ValidationIssue] = []
        
        # Patterns to detect hacky implementations
        self.hacky_patterns = {
            r"_fix\.py$": "Files with '_fix' suffix suggest hacky patches",
            r"_hack\.py$": "Files with '_hack' suffix suggest hacky code",
            r"_temp\.py$": "Files with '_temp' suffix suggest temporary code",
            r"_old\.py$": "Files with '_old' suffix suggest deprecated code",
            r"TODO.*HACK": "TODO comments mentioning HACK",
            r"FIXME.*HACK": "FIXME comments mentioning HACK",
            r"XXX.*HACK": "XXX comments mentioning HACK",
            r"# CUTRE": "Comments explicitly mentioning 'CUTRE'",
            r"# HACK:": "Comments explicitly mentioning HACK",
            r"# TEMPORARY": "Temporary code markers",
            r"import\s+sys\s*\n\s*sys\.path\.insert": "Manual sys.path manipulation (bad practice)",
            r"logging\.getLogger\(__name__\).*\n(?!.*logger\.setLevel|.*logger\.addHandler)": 
                "Logger created but never configured",
        }
        
        # Required exports for each component
        self.required_exports = {
            "luminoracore-sdk-python/luminoracore_sdk/__init__.py": [
                "setup_logging", "LuminoraCoreClient", "LuminoraCoreClientV11"
            ],
            "luminoracore/luminoracore/__init__.py": [
                "setup_logging", "Personality"
            ],
            "luminoracore-cli/luminoracore_cli/__init__.py": [
                "setup_logging"
            ]
        }
        
        # Files that should NOT exist
        self.forbidden_files = [
            "*_fix.py",
            "*_hack.py",
            "*_temp.py",
            "*.bak",
            "*.old"
        ]
    
    def validate(self) -> bool:
        """Run all validations. Returns True if all checks pass."""
        print("🔍 Starting LuminoraCore Framework Validation...")
        print("=" * 80)
        
        # Run all validation checks
        self._check_forbidden_files()
        self._check_logging_configuration()
        self._check_required_exports()
        self._check_code_quality()
        self._check_database_support()
        self._check_llm_provider_support()
        self._check_documentation()
        
        # Print results
        self._print_results()
        
        # Return overall status
        critical_issues = [i for i in self.issues if i.severity == Severity.CRITICAL]
        return len(critical_issues) == 0
    
    def _check_forbidden_files(self):
        """Check for files that should not exist."""
        print("\n📁 Checking for forbidden files...")
        
        for pattern in self.forbidden_files:
            for file_path in self.root_path.rglob(pattern):
                # Skip common directories
                if any(skip in str(file_path) for skip in ['.git', '__pycache__', 'venv', 'node_modules']):
                    continue
                
                self.issues.append(ValidationIssue(
                    severity=Severity.CRITICAL,
                    category="Forbidden Files",
                    file_path=str(file_path.relative_to(self.root_path)),
                    line_number=None,
                    description=f"Forbidden file found: {file_path.name}",
                    suggestion=f"Remove this file or rename it without '{pattern[1:-3]}' suffix"
                ))
        
        print(f"  ✓ Forbidden files check complete")
    
    def _check_logging_configuration(self):
        """Check that logging is properly configured."""
        print("\n📝 Checking logging configuration...")
        
        components = [
            ("luminoracore-sdk-python", "luminoracore_sdk"),
            ("luminoracore", "luminoracore"),
            ("luminoracore-cli", "luminoracore_cli")
        ]
        
        for component_dir, package_name in components:
            # Check for logging_config.py
            logging_config_path = self.root_path / component_dir / package_name / "logging_config.py"
            
            if not logging_config_path.exists():
                self.issues.append(ValidationIssue(
                    severity=Severity.CRITICAL,
                    category="Logging Configuration",
                    file_path=f"{component_dir}/{package_name}",
                    line_number=None,
                    description=f"Missing logging_config.py in {package_name}",
                    suggestion=f"Add logging_config.py module to {component_dir}/{package_name}/"
                ))
            else:
                # Check content
                try:
                    content = logging_config_path.read_text(encoding='utf-8')
                except UnicodeDecodeError:
                    continue
                
                if "setup_logging" not in content:
                    self.issues.append(ValidationIssue(
                        severity=Severity.HIGH,
                        category="Logging Configuration",
                        file_path=str(logging_config_path.relative_to(self.root_path)),
                        line_number=None,
                        description="logging_config.py missing 'setup_logging' function",
                        suggestion="Add setup_logging() function to logging_config.py"
                    ))
                
                if "auto_configure" not in content:
                    self.issues.append(ValidationIssue(
                        severity=Severity.MEDIUM,
                        category="Logging Configuration",
                        file_path=str(logging_config_path.relative_to(self.root_path)),
                        line_number=None,
                        description="logging_config.py missing 'auto_configure' function",
                        suggestion="Add auto_configure() function to logging_config.py"
                    ))
        
        print(f"  ✓ Logging configuration check complete")
    
    def _check_required_exports(self):
        """Check that required functions are exported."""
        print("\n📦 Checking required exports...")
        
        for file_path, required in self.required_exports.items():
            full_path = self.root_path / file_path
            
            if not full_path.exists():
                self.issues.append(ValidationIssue(
                    severity=Severity.CRITICAL,
                    category="Required Exports",
                    file_path=file_path,
                    line_number=None,
                    description=f"Required file not found: {file_path}",
                    suggestion=f"Create {file_path} with required exports"
                ))
                continue
            
            try:
                content = full_path.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                continue
            
            for export in required:
                if export not in content:
                    self.issues.append(ValidationIssue(
                        severity=Severity.HIGH,
                        category="Required Exports",
                        file_path=file_path,
                        line_number=None,
                        description=f"Missing required export: {export}",
                        suggestion=f"Add '{export}' to __all__ in {file_path}"
                    ))
        
        print(f"  ✓ Required exports check complete")
    
    def _check_code_quality(self):
        """Check code quality issues."""
        print("\n🔧 Checking code quality...")
        
        python_files = list(self.root_path.rglob("*.py"))
        
        for file_path in python_files:
            # Skip common directories
            if any(skip in str(file_path) for skip in ['.git', '__pycache__', 'venv', 'node_modules', '.pytest_cache']):
                continue
            
            try:
                content = file_path.read_text(encoding='utf-8')
                lines = content.split('\n')
                
                # Check for hacky patterns
                for line_num, line in enumerate(lines, 1):
                    for pattern, description in self.hacky_patterns.items():
                        if re.search(pattern, line, re.IGNORECASE):
                            self.issues.append(ValidationIssue(
                                severity=Severity.MEDIUM,
                                category="Code Quality",
                                file_path=str(file_path.relative_to(self.root_path)),
                                line_number=line_num,
                                description=description,
                                suggestion="Refactor to use proper implementation"
                            ))
            
            except Exception as e:
                # Skip files we can't read
                pass
        
        print(f"  ✓ Code quality check complete")
    
    def _check_database_support(self):
        """Check that all databases are properly supported."""
        print("\n💾 Checking database support...")
        
        databases = [
            "dynamodb",
            "sqlite",
            "postgresql",
            "redis",
            "mongodb"
        ]
        
        sdk_session_path = self.root_path / "luminoracore-sdk-python" / "luminoracore_sdk" / "session"
        
        for db in databases:
            storage_file = sdk_session_path / f"storage_{db}_flexible.py"
            
            if not storage_file.exists():
                self.issues.append(ValidationIssue(
                    severity=Severity.HIGH,
                    category="Database Support",
                    file_path=str(sdk_session_path.relative_to(self.root_path)),
                    line_number=None,
                    description=f"Missing flexible storage implementation for {db}",
                    suggestion=f"Create storage_{db}_flexible.py with proper implementation"
                ))
            else:
                # Check content
                try:
                    content = storage_file.read_text(encoding='utf-8')
                except UnicodeDecodeError:
                    continue
                
                if "Flexible" not in content:
                    self.issues.append(ValidationIssue(
                        severity=Severity.MEDIUM,
                        category="Database Support",
                        file_path=str(storage_file.relative_to(self.root_path)),
                        line_number=None,
                        description=f"Storage implementation for {db} not flexible",
                        suggestion="Ensure storage supports any database schema"
                    ))
                
                # Check for logging
                if "logger" not in content and "logging" not in content:
                    self.issues.append(ValidationIssue(
                        severity=Severity.LOW,
                        category="Database Support",
                        file_path=str(storage_file.relative_to(self.root_path)),
                        line_number=None,
                        description=f"Storage implementation for {db} has no logging",
                        suggestion="Add logging to storage implementation"
                    ))
        
        print(f"  ✓ Database support check complete")
    
    def _check_llm_provider_support(self):
        """Check that all LLM providers are properly supported."""
        print("\n🤖 Checking LLM provider support...")
        
        providers = [
            "openai",
            "anthropic",
            "deepseek",
            "google",
            "mistral"
        ]
        
        sdk_providers_path = self.root_path / "luminoracore-sdk-python" / "luminoracore_sdk" / "providers"
        
        for provider in providers:
            provider_file = sdk_providers_path / f"{provider}.py"
            
            if not provider_file.exists():
                self.issues.append(ValidationIssue(
                    severity=Severity.MEDIUM,
                    category="LLM Provider Support",
                    file_path=str(sdk_providers_path.relative_to(self.root_path)),
                    line_number=None,
                    description=f"Missing provider implementation for {provider}",
                    suggestion=f"Create {provider}.py with proper implementation"
                ))
            else:
                # Check content
                try:
                    content = provider_file.read_text(encoding='utf-8')
                except UnicodeDecodeError:
                    continue
                
                # Check for logging
                if "logger" not in content and "logging" not in content:
                    self.issues.append(ValidationIssue(
                        severity=Severity.LOW,
                        category="LLM Provider Support",
                        file_path=str(provider_file.relative_to(self.root_path)),
                        line_number=None,
                        description=f"Provider {provider} has no logging",
                        suggestion="Add logging to provider implementation"
                    ))
        
        print(f"  ✓ LLM provider support check complete")
    
    def _check_documentation(self):
        """Check documentation completeness."""
        print("\n📚 Checking documentation...")
        
        required_docs = [
            "README.md",
            "INSTALLATION_GUIDE.md",
            "QUICK_START.md",
            "luminoracore-sdk-python/docs/api_reference.md",
            "luminoracore-sdk-python/README.md",
            "luminoracore/README.md",
            "luminoracore-cli/README.md"
        ]
        
        for doc_path in required_docs:
            full_path = self.root_path / doc_path
            
            if not full_path.exists():
                self.issues.append(ValidationIssue(
                    severity=Severity.MEDIUM,
                    category="Documentation",
                    file_path=doc_path,
                    line_number=None,
                    description=f"Missing documentation: {doc_path}",
                    suggestion=f"Create {doc_path} with complete documentation"
                ))
            else:
                try:
                    content = full_path.read_text(encoding='utf-8')
                except UnicodeDecodeError:
                    # Skip files with encoding issues
                    continue
                
                # Check for setup_logging documentation
                if "sdk" in doc_path.lower() and "setup_logging" not in content:
                    self.issues.append(ValidationIssue(
                        severity=Severity.LOW,
                        category="Documentation",
                        file_path=doc_path,
                        line_number=None,
                        description="Documentation missing setup_logging information",
                        suggestion="Add section about setup_logging() function"
                    ))
        
        print(f"  ✓ Documentation check complete")
    
    def _print_results(self):
        """Print validation results."""
        print("\n" + "=" * 80)
        print("📊 VALIDATION RESULTS")
        print("=" * 80)
        
        if not self.issues:
            print("\n✅ ALL CHECKS PASSED! Framework is professional and clean.")
            return
        
        # Group issues by severity
        issues_by_severity = {}
        for issue in self.issues:
            if issue.severity not in issues_by_severity:
                issues_by_severity[issue.severity] = []
            issues_by_severity[issue.severity].append(issue)
        
        # Print summary
        print(f"\n🔍 Found {len(self.issues)} issues:")
        for severity in Severity:
            count = len(issues_by_severity.get(severity, []))
            if count > 0:
                emoji = {
                    Severity.CRITICAL: "🔴",
                    Severity.HIGH: "🟠",
                    Severity.MEDIUM: "🟡",
                    Severity.LOW: "🔵",
                    Severity.INFO: "ℹ️"
                }[severity]
                print(f"  {emoji} {severity.value}: {count}")
        
        # Print detailed issues
        for severity in Severity:
            issues = issues_by_severity.get(severity, [])
            if not issues:
                continue
            
            print(f"\n{severity.value} ISSUES:")
            print("-" * 80)
            
            for i, issue in enumerate(issues, 1):
                print(f"\n{i}. [{issue.category}] {issue.description}")
                print(f"   File: {issue.file_path}")
                if issue.line_number:
                    print(f"   Line: {issue.line_number}")
                print(f"   💡 Suggestion: {issue.suggestion}")
        
        # Print action items
        critical_count = len(issues_by_severity.get(Severity.CRITICAL, []))
        high_count = len(issues_by_severity.get(Severity.HIGH, []))
        
        print("\n" + "=" * 80)
        print("🎯 ACTION ITEMS:")
        print("=" * 80)
        
        if critical_count > 0:
            print(f"\n❌ {critical_count} CRITICAL issues MUST be fixed before release")
        
        if high_count > 0:
            print(f"\n⚠️  {high_count} HIGH priority issues should be fixed")
        
        print("\nRun this script again after making fixes to verify.")
    
    def export_report(self, output_file: str = "validation_report.json"):
        """Export validation report to JSON file."""
        report = {
            "total_issues": len(self.issues),
            "by_severity": {},
            "by_category": {},
            "issues": []
        }
        
        # Count by severity
        for severity in Severity:
            count = len([i for i in self.issues if i.severity == severity])
            report["by_severity"][severity.value] = count
        
        # Count by category
        categories = set(i.category for i in self.issues)
        for category in categories:
            count = len([i for i in self.issues if i.category == category])
            report["by_category"][category] = count
        
        # Add all issues
        for issue in self.issues:
            report["issues"].append({
                "severity": issue.severity.value,
                "category": issue.category,
                "file": issue.file_path,
                "line": issue.line_number,
                "description": issue.description,
                "suggestion": issue.suggestion
            })
        
        # Write to file
        output_path = self.root_path / output_file
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Report exported to: {output_file}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Validate LuminoraCore framework for professional standards"
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Root directory of the framework (default: current directory)"
    )
    parser.add_argument(
        "--export",
        default=None,
        help="Export report to JSON file (default: validation_report.json)"
    )
    
    args = parser.parse_args()
    
    # Create validator
    validator = FrameworkValidator(root_path=args.root)
    
    # Run validation
    success = validator.validate()
    
    # Export report if requested
    if args.export or not success:
        output_file = args.export or "validation_report.json"
        validator.export_report(output_file)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
