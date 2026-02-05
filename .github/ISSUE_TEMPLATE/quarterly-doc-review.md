---
name: Quarterly Documentation Review
about: Template for quarterly documentation maintenance and updates
title: '[DOC REVIEW] Q[X] 2026 Documentation Review'
labels: documentation, maintenance
assignees: ''
---

## 📅 Quarterly Documentation Review - Q[X] 2026

**Review Period**: [Start Date] - [End Date]  
**Target Completion**: [Target Date]  
**Copilot Studio Version**: [Current Version as of review]  
**Reviewer**: [Assigned Reviewer]

---

## 🎯 Objectives

This quarterly review ensures our documentation remains aligned with the latest Microsoft Copilot Studio UI, features, and best practices.

### Official Release Notes to Review:
- [ ] [Power Platform Release Plan](https://learn.microsoft.com/power-platform/release-plan/)
- [ ] [Copilot Studio What's New](https://learn.microsoft.com/microsoft-copilot-studio/whats-new)
- [ ] [Microsoft Graph API Changelog](https://learn.microsoft.com/graph/changelog)
- [ ] [Power Automate Updates](https://learn.microsoft.com/power-automate/whats-new)

---

## 📋 Documentation Review Checklist

### Priority 1: Critical Documentation (Update within 1 week)

#### ✅ COPILOT-STUDIO-IMPLEMENTATION.md
- [ ] Verify environment setup steps match current UI
- [ ] Check agent creation wizard flow
- [ ] Validate topic configuration examples
- [ ] Update entity and variable sections
- [ ] Test all Power Automate integration steps
- [ ] Review screenshots for UI accuracy
- [ ] Verify Chinese and English translations are consistent
- [ ] Update "Last Updated" date
- [ ] Check all links to Microsoft docs

**Notes**: 
```
[Add any discrepancies found]
```

#### ✅ README.md
- [ ] Update version numbers
- [ ] Verify quick start commands work
- [ ] Check license and feature availability
- [ ] Update performance metrics if changed
- [ ] Verify all documentation links
- [ ] Update "Last Updated" date

**Notes**:
```
[Add any discrepancies found]
```

#### ✅ COPILOT-STUDIO-CHECKLIST.md
- [ ] Verify all checklist items are current
- [ ] Update any changed configuration steps
- [ ] Add new features or capabilities
- [ ] Remove deprecated items
- [ ] Update "Last Updated" date

**Notes**:
```
[Add any discrepancies found]
```

### Priority 2: High Priority Documentation (Update within 2 weeks)

#### ✅ agent-team-design.md
- [ ] Verify agent capabilities are current
- [ ] Check for new connector options
- [ ] Update prompt engineering best practices
- [ ] Review tool configurations
- [ ] Add new features to agent descriptions

**Notes**:
```
[Add any discrepancies found]
```

#### ✅ ENTERPRISE-GUIDE.md
- [ ] Check security recommendations
- [ ] Verify compliance requirements
- [ ] Update governance best practices
- [ ] Review license requirements
- [ ] Check deployment strategies

**Notes**:
```
[Add any discrepancies found]
```

#### ✅ DEPLOYMENT-GUIDE.md
- [ ] Test deployment scripts
- [ ] Verify Azure configurations
- [ ] Check authentication methods
- [ ] Update prerequisites
- [ ] Validate troubleshooting steps

**Notes**:
```
[Add any discrepancies found]
```

### Priority 3: Medium Priority Documentation (Update within 4 weeks)

#### ✅ SECURITY.md
- [ ] Review security best practices
- [ ] Check for new security features
- [ ] Update threat models
- [ ] Verify compliance certifications

**Notes**:
```
[Add any discrepancies found]
```

#### ✅ architecture-documentation.md
- [ ] Verify technical architecture diagrams
- [ ] Update API references
- [ ] Check data flow descriptions
- [ ] Review integration patterns

**Notes**:
```
[Add any discrepancies found]
```

#### ✅ Other Documentation Files
- [ ] CONTRIBUTING.md
- [ ] 資料完備性評估.md
- [ ] agent-configurations.json
- [ ] Other docs/ files

**Notes**:
```
[Add any discrepancies found]
```

---

## 🔍 UI and Feature Changes

### New Features to Document:
- [ ] [Feature 1]
- [ ] [Feature 2]
- [ ] [Feature 3]

### Deprecated Features to Remove:
- [ ] [Feature 1]
- [ ] [Feature 2]

### UI Changes Observed:
- [ ] [Change 1]
- [ ] [Change 2]

---

## 🔗 Broken Links Check

Use link checker tool to verify all external links:
- [ ] Run link checker: `npm run check-links` or manual check
- [ ] Fix or remove broken links
- [ ] Update redirected URLs
- [ ] Verify Microsoft Learn links

**Broken Links Found**:
```
[List any broken links]
```

---

## 🧪 Testing in Live Environment

### Test Environment:
- **Tenant**: [Tenant name/ID]
- **Environment**: [Environment name]
- **Copilot Studio Version**: [Version]
- **Date Tested**: [Date]

### Test Scenarios Verified:
- [ ] Create new agent from scratch following guide
- [ ] Configure topics and entities
- [ ] Set up Power Automate flows
- [ ] Test agent handoff functionality
- [ ] Verify security configurations
- [ ] Test end-to-end user scenario

**Issues Found**:
```
[Describe any issues encountered]
```

---

## 📊 Community Feedback Review

### Open Issues with `documentation-outdated` Label:
- [ ] [Issue #XX](link) - [Description]
- [ ] [Issue #XX](link) - [Description]
- [ ] [Issue #XX](link) - [Description]

### Recent Discussions:
- [ ] [Discussion #XX](link) - [Description]
- [ ] [Discussion #XX](link) - [Description]

### Action Items:
```
[List actions needed based on community feedback]
```

---

## 📝 Update Summary

### Documents Updated:
- [ ] [Document name] - [Brief description of changes]
- [ ] [Document name] - [Brief description of changes]

### Version Changes:
- Previous documentation version: [X.X.X]
- New documentation version: [X.X.X]

### CHANGELOG.md Updated:
- [ ] Added new version entry
- [ ] Documented all major changes
- [ ] Updated "Last Updated" dates

---

## ✅ Review Completion

### Sign-off:
- [ ] All Priority 1 documentation reviewed and updated
- [ ] All Priority 2 documentation reviewed and updated
- [ ] All Priority 3 documentation reviewed and updated
- [ ] Broken links fixed
- [ ] Community issues addressed
- [ ] CHANGELOG.md updated
- [ ] Testing completed successfully
- [ ] Pull request created with all changes
- [ ] Ready for final approval

**Reviewer**: [Name]  
**Date Completed**: [Date]  
**Next Review Date**: [Next Quarter Date]

---

## 📎 Additional Notes

```
[Add any additional observations, recommendations, or notes]
```

---

## 🔄 Next Quarter Planning

### Anticipated Changes:
- [ ] [Expected feature release]
- [ ] [Expected UI updates]

### Preparation Tasks:
- [ ] [Task 1]
- [ ] [Task 2]

---

**Reference**: See [DOCS-MAINTENANCE.md](../../DOCS-MAINTENANCE.md) for detailed maintenance guidelines.
