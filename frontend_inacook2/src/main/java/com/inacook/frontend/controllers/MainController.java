package com.inacook.frontend.controllers;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class MainController {

    @GetMapping({"/", "/dashboard"})
    public String dashboard(Model model){
        model.addAttribute("nombre","Usuario");
        model.addAttribute("rol","Alumno");
        return "dashboard";
    }

    @GetMapping("/ver_recetas")
    public String verRecetas(){
        return "ver_recetas";
    }

    @GetMapping("/subir_receta")
    public String subirReceta(){
        return "subir_receta";
    }

    @GetMapping("/calculadora")
    public String calculadora(){
        return "calculadora";
    }

    @GetMapping("/login")
    public String login(){
        return "login";
    }

    @GetMapping("/register")
    public String register(){
        return "register";
    }

    @GetMapping("/perfil")
    public String perfil(Model model){
        model.addAttribute("usuarioNombre","usuario_demo");
        model.addAttribute("rol","Alumno");
        return "perfil";
    }

    @GetMapping("/crear_ingrediente")
    public String crearIngrediente(){
        return "crear_ingrediente";
    }

    @GetMapping("/ver_ingredientes")
    public String verIngredientes(){
        return "ver_ingredientes";
    }

    @GetMapping("/ver_recetas_alumnos")
    public String verRecetasAlumnos(){
        return "ver_recetas_alumnos";
    }

    @GetMapping("/ver_historial")
    public String verHistorial(){
        return "ver_historial";
    }

    @GetMapping("/comprobante_receta")
    public String comprobante(){
        return "comprobante_receta";
    }

    @GetMapping("/borrar_receta")
    public String borrarReceta(){
        return "borrar_receta";
    }

    @GetMapping("/cambiar_contraseña")
    public String cambiarContrasenna(){
        return "cambiar_contraseña";
    }
}
