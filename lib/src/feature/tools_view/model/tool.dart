import 'package:flutter/material.dart';

class ToolModel {
  final String title;
  final IconData icon;
  final Function() onTap;

  ToolModel({required this.title, required this.icon, required this.onTap});
}
