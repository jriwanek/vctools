#include <stdint.h>
#include "vc4_data.h"

vc4_emul_init (void *user_data) {
  

  
  
  



vc4_emul_free (struct vc4_emul *emul) {
  

vc4_emul_exec (struct vc4_emul *emul, unsigned int steps) {
  

  
    
  



vc4_emul_exception (struct vc4_emul *emul, 
                    
  
//    uint16_t instr;
  int i;

  
  
    
  
  



vc4_emul_set_scalar_reg (struct vc4_emul *emul, int reg, uint32_t value) {
  
  


  
  


  
  
       && reg == REGISTER_SP) {
    
  
  



_set_reg (struct vc4_emul *emul, int reg, uint32_t value) {
  
  
       && reg == REGISTER_SP) {
    
  
  
    
  
  
    /*
     * print_log("r%d <= %08x\\n", reg, value);
     */ 
    emul->scalar_regs[reg] = value;


  
  
    
  
    
  



int_to_float (uint32_t x) {
  


  




/* memory access functions */ 
  int
size (int format) {
  
  
    
  
  
    
  
    
  
    
  


  
  

  
    
      /*
       * TODO: Is this the correct exception number? 
       */ 
      interrupt (1, "load: invalid alignment.");
  
  
  
    
  
  



_store (struct vc4_emul *emul, 
        
  

  
    
      /*
       * TODO: Is this the correct exception number? 
       */ 
      interrupt (1, "store: invalid alignment.");
  
  



_push (struct vc4_emul *emul, uint32_t value) {
  
  


  
  
  


